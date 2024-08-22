from connect import *
import warnings

from tkinter import ttk
from tkinter import *
import tkinter as tk
from connect import *

def MyRoi(name, rcolor, rtype, plan, threshold, dose):
	try: 
		roi = case.PatientModel.CreateRoi(Name = name, Color = rcolor, Type = rtype)
		roi.CreateRoiGeometryFromDose(DoseDistribution = dose, \
		ThresholdLevel = threshold)
	
	except:
		print(str(name+" ROI already exists"))
	
	case.TreatmentPlans[plan].TreatmentCourse.TotalDose.UpdateDoseGridStructures()

def AlgebraRoi(name, RoiA, RoiB, operation, rcolor, rtype, examination):
		try:		
			roi_int = case.PatientModel.CreateRoi(Name=name, Color=rcolor, Type=rtype, TissueName=None, RbeCellTypeName=None, RoiMaterial=None)
			# The type of operation is called "Intersection"		
			roi_int.SetAlgebraExpression(\
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [RoiA], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, \
			'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, \
	   
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [RoiB], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, \
			'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, \
	   
			ResultOperation=operation, ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, \
			'Posterior': 0, 'Right': 0, 'Left': 0 })
			
			roi_int.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
		except:
			print(str(operation+' ROI already exists'))

case=get_current("Case")
ExNames=case.Examinations._ #List all the examinations
nEx = len(ExNames.split()) #Count the total number of examinations
Names=[]
for i in range(0,nEx):
	Names.append(case.Examinations[i].Name)

# The following windows allow for SPECT and PET image (examination) selection	
def ComboboxSelection():
    app = tk.Tk()
    app.title("Select the examinations")
    app.geometry('350x120')
    Selection=ComboboxSelectionWindow(app)
    app.mainloop()

    return Selection.comboBox_example_contents
    
class ComboboxSelectionWindow():
    def __init__(self, master):
        self.master=master
        self.entry_contents=None
        self.labelTop = tk.Label(master,text = "Select the SPECT image")
        self.labelTop.place(x = 20, y = 10, width=140, height=20)
        self.comboBox_example = ttk.Combobox(master,values=Names,
	    state="readonly",)
        self.comboBox_example.current(0)
        self.comboBox_example.place(x = 105, y = 35, width=140, height=25)

        self.okButton = tk.Button(master, text='OK',command = self.callback)
        self.okButton.place(x = 105, y = 70, width=140, height=25)

    def callback(self):#get the contents of the Entry and exit
        self.comboBox_example_contents=self.comboBox_example.get()
        self.master.destroy()

ES=ComboboxSelection() # SPECT examination's name


class ComboboxSelectionWindow():
    def __init__(self, master):
        self.master=master
        self.entry_contents=None
        self.labelTop = tk.Label(master,text = "Select the PET image")
        self.labelTop.place(x = 20, y = 10, width=140, height=20)
        self.comboBox_example = ttk.Combobox(master,values=Names,
	    state="readonly",)
        self.comboBox_example.current(0)
        self.comboBox_example.place(x = 105, y = 35, width=140, height=25)

        self.okButton = tk.Button(master, text='OK',command = self.callback)
        self.okButton.place(x = 105, y = 70, width=140, height=25)

    def callback(self):#get the contents of the Entry and exit
        self.comboBox_example_contents=self.comboBox_example.get()
        self.master.destroy()

EP=ComboboxSelection() #PET examination's name

with CompositeAction("Get the plans that use the PET and SPECT examinations"):
	PlanNames = case.TreatmentPlans._ 
	nPlan = len(PlanNames.split()) 
	BeamSetS=""
	BeamSetP=""
	for ex in range(0,nPlan,1):
		bs=case.TreatmentPlans[ex].BeamSets[0].GetPlanningExamination()#get the image set used by this plan
		beam=str(bs)
		if(ES in beam):
			BeamSetS=case.TreatmentPlans[ex]#SPECT BeamSet
		elif(EP in beam):
			BeamSetP=case.TreatmentPlans[ex]#SPECT BeamSet
	
with CompositeAction("Check that the 'Scaled' plans do not already exist"):
	PS='SPECT Scaled'
	PSExists=0
	PP='PET Scaled'	
	PPExists=0
	
	for iPlan in range(0,nPlan):
		if (case.TreatmentPlans[iPlan].Name == PS): 
			PSExists=1
		elif (case.TreatmentPlans[iPlan].Name == PP):
			PPExists=1
	
with CompositeAction("Copy the plans"):
	if (PSExists==0): #"SPECT Scaled" doesn't exist
		case.CopyPlan(PlanName=BeamSetS.Name, NewPlanName=PS, KeepBeamSetNames=False)

	if (PPExists==0):#"PET Scaled" doesn't exist
		case.CopyPlan(PlanName=BeamSetP.Name, NewPlanName=PP, KeepBeamSetNames=False)

with CompositeAction('Create external ROIs for each plan'):
	# SPECT
	try:
		roi_spect = case.PatientModel.CreateRoi(Name="External SPECT", Color="Green", Type="External", TissueName="", RbeCellTypeName=None, RoiMaterial=None)
		roi_spect.CreateExternalGeometries(ReferenceExamination=case.Examinations[ES], AdditionalExaminationNames=[EP], ReferenceThresholdLevel=-250)
		
	except:
		print('External SPECT already exists')
	
	# PET
	try:
		roi_pet = case.PatientModel.CreateRoi(Name="External PET", Color="Green", Type="External", TissueName="", RbeCellTypeName=None, RoiMaterial=None)
		roi_pet.CreateExternalGeometries(ReferenceExamination=case.Examinations[EP], AdditionalExaminationNames=[ES], ReferenceThresholdLevel=-250)
		
	except:
		print('External PET already exists')

#Update the geometries
case.TreatmentPlans[PS].TreatmentCourse.TotalDose.UpdateDoseGridStructures()
case.TreatmentPlans[PP].TreatmentCourse.TotalDose.UpdateDoseGridStructures()

with CompositeAction('Normalize the dose maps to the maximum value'):
	#  SPECT
	if (PSExists==0):
		case.TreatmentPlans[PS].BeamSets[PS].ScaleToDoseGoal(DspName=None, RoiName="External SPECT", DoseValue=10000, DoseVolume=0,\
		PrescriptionType="DoseAtVolume", LockedBeamNames=None, EvaluateOptimizationFunctionsAfterScaling=True, IncludeBackgroundDose=False)
	# PET
	if (PPExists==0):
		case.TreatmentPlans[PP].BeamSets[PP].ScaleToDoseGoal(DspName=None, RoiName="External PET", DoseValue=10000, DoseVolume=0,\
		PrescriptionType="DoseAtVolume", LockedBeamNames=None, EvaluateOptimizationFunctionsAfterScaling=True, IncludeBackgroundDose=False)
# After the PET's dose is deformed using the deformable registration, the maximum dose value may change in the "PET Scaled" deformed evaluation dose. To avoid any issues, 
# the threshold values will be normalized again when creating the ROIs further down the script

with CompositeAction('Check if a frame of reference between the SPECT and PET examinations already exists'):
	Names = case.StructureRegistrations._ 
	nFOR = len(Names.split()) 
	FORIndex=-1
	fo=0
	for fo in range(0,nFOR):
	#The "case.Registration._" function doesn't work, so the FoR names are obtained from the "case.StructureRegistrations.-" objects, using the "FromExamination" and "ToExaminaition" function
		fromname=case.StructureRegistrations[fo].FromExamination.Name #Must be the SPECT examination (ES)
		toname=case.StructureRegistrations[fo].ToExamination.Name #Must be the PET examination (EP)
		grid=case.StructureRegistrations[fo].DeformationGrid.FrameOfReference #Defomaion grid corresponding to a deformable registration
		if(fromname==ES and toname==EP and grid==""):#The last condition ensures that only the 'Source registration' registrations are picked
			FORIndex=fo # Frame of reference index. If the FoR doesn't already exist, the index value will be -1	
			
with CompositeAction('Create a rigid registration if necessary'):		
	if(FORIndex==-1):
		case.CreateNamedIdentityFrameOfReferenceRegistration(FromExaminationName=EP, ToExaminationName=ES, RegistrationName="FoR PET to SPECT", \
		Description=None)
	
		#Image registration
		case.ComputeGrayLevelBasedRigidRegistration(FloatingExaminationName=EP, ReferenceExaminationName=ES, RegistrationName=None, \
		UseOnlyTranslations=False, HighWeightOnBones=True, InitializeImages=True, FocusRoisNames=[])

with CompositeAction('Check for radioembolization deformable registrations (DefRegRadioembolization)'):	
	RegGr=case.PatientModel.StructureRegistrationGroups._
	nRegGr = len(RegGr.split()) 
	gr=0
	RegGroupExists=-1 # if RegGrIndex==-1 there isn't any deformable registration with the "DefRegRemb" name
	nRegDef=-1
	while gr < nRegGr: #This assigns a free index to the new registration group
		RegGrTitle=case.PatientModel.StructureRegistrationGroups[gr].Name
		if ('DefRegRadioembolization' in RegGrTitle):
			RegGroupExists=gr 
			break
		gr+=1

with CompositeAction('Create a deformable regristration with a new index'):	
	GrName=str("DefRegRadioembolization")
	DefName=str("DefRegRadioembolization1")
	
	if(RegGroupExists==-1):#If a deformabele registration doesn't exist
		case.PatientModel.CreateHybridDeformableRegistrationGroup(RegistrationGroupName=GrName, ReferenceExaminationName=ES, \
		TargetExaminationNames=[EP], ControllingRoiNames=[], ControllingPoiNames=[], FocusRoiNames=[], \
		AlgorithmSettings={ 'NumberOfResolutionLevels': 3, 'InitialResolution': { 'x': 0.5, 'y': 0.5, 'z': 0.5 }, \
		'FinalResolution': { 'x': 0.25, 'y': 0.25, 'z': 0.25 }, 'InitialGaussianSmoothingSigma': 2, 'FinalGaussianSmoothingSigma': 0.333333333333333, \
		'InitialGridRegularizationWeight': 400, 'FinalGridRegularizationWeight': 400, 'ControllingRoiWeight': 0.5, 'ControllingPoiWeight': 0.1, \
		'MaxNumberOfIterationsPerResolutionLevel': 1000, 'ImageSimilarityMeasure': "MutualInformation", 'DeformationStrategy': "Default", \
		'ConvergenceTolerance': 1E-05 })



with CompositeAction('Find the deformed PET dose map index'):
	DoseOnEx=case.TreatmentDelivery.FractionEvaluations[0]
	DoseOnExNames = DoseOnEx.DoseOnExaminations._ 
	nDoseOnEx = len(DoseOnExNames.split()) 
	DoseOnExSPECTIndex=0 
	ex=0
	DoseEvPlanExists=-1 #to check and obtain the index of the 'PET Scaled' deformed dose
	while ex < nDoseOnEx:
		DoseOnExTitle=DoseOnEx.DoseOnExaminations[ex].OnExamination.Name
		if len(DoseOnExTitle)==0:
			ex+=1
		if DoseOnExTitle == ES:
			DoseOnExSPECTIndex=ex
			DoseOnExSPECT=case.TreatmentDelivery.FractionEvaluations[0].DoseOnExaminations[DoseOnExSPECTIndex]
			DoseEvNames=DoseOnExSPECT.DoseEvaluations._
			nDoseEv = len(DoseEvNames.split()) 
			DoseEvRembIndex=0
			
			ev=0
			while ev<nDoseEv:
				DoseEvTitle=DoseOnExSPECT.DoseEvaluations[ev].ByStructureRegistration.Name
				DoseEvPlan=DoseOnExSPECT.DoseEvaluations[ev].OfDoseDistribution.ForBeamSet.DicomPlanLabel
				if len(DoseEvTitle)==0:
					ev+=1
				if DoseEvTitle == DefName and DoseEvPlan == PP:
					DoseEvRembIndex=ev
					DoseEvPlanExists=1
					break
					break
			ev+=1
		ex += 1	


with CompositeAction("Deform PET's dose map"):
	if DoseEvPlanExists ==-1: 
		# Deform the "PET Scaled" dose map using the deformation registration
		beam_pet=case.TreatmentPlans[PP].BeamSets[PP]
		case.MapDose(FractionNumber=0, SetTotalDoseEstimateReference=True, DoseDistribution=beam_pet.FractionDose,\
		StructureRegistration=case.StructureRegistrations[DefName], ReferenceDoseGrid=None)
		case.TreatmentPlans[PS].TreatmentCourse.TotalDose.UpdateDoseGridStructures()
	else:
		print("'PET Scaled' dose map already deformed")
# Update dose statistics
case.TreatmentPlans[PS].TreatmentCourse.TotalDose.UpdateDoseGridStructures()
case.TreatmentPlans[PP].TreatmentCourse.TotalDose.UpdateDoseGridStructures()

with CompositeAction('Create the PET and SPECT threshold dose ROIs'):
	examination=case.Examinations[ES] 
	plan=case.TreatmentPlans[PS]
	plan_dose_pet=case.TreatmentDelivery.FractionEvaluations[0].DoseOnExaminations[DoseOnExSPECTIndex].DoseEvaluations[DoseEvRembIndex]
	# As the PET maximum dose value may change after the dose map is deformed, this will ensure the threshold values are normalized to 
	# the new maximum value
	dosemax=plan_dose_pet.GetDoseStatistic(RoiName="External PET", DoseType="Max")
	# The created ROIs with range from 10 to 90% of the maximum dose, by steps of 10%
	initial = 10
	final = 100
	step=10
			
with CompositeAction('Create the PET and SPECT threshold dose ROIs'):	
	for j in range(initial,final,step):
		threshold_level =j*100
		# PET # The voxel dose values are multiplied by 100. Thus, the threshold dose vaues must be multiplied by 100
		roi_pet = str(str(j)+"P")
		MyRoi(roi_pet, 'Green', 'Control', PS, threshold_level*NormPetDose, plan_dose_pet)
		
		#SPECT
		roi_spect = str(str(j)+"S")
		MyRoi(roi_spect, 'Blue', 'Control', PS, threshold_level, plan_dose_spect)
		
		# Overlapping volume
		roi_over=str(j)+' over.'
		AlgebraRoi(roi_over, roi_pet, roi_spect, "Intersection", "White", "Control", examination)
		
		# Non-overlapping volume
		roi_nonover=str(j)+' non over.'
		AlgebraRoi(roi_nonover, roi_pet, roi_spect, "Subtraction", "Red", "Control", examination)
		
with CompositeAction('Image registration verification'):
# Verify that the Jacobian determinant of the transformation matrix at each voxel verifies the aceptability condition (det(J)>0)
	m=case.StructureRegistrations[DefName].ComputeJacobianDeterminantForROI(RoiName="External PET")
	max=len(m)
	invalid=0
	for i in range(0,max,1):
		if (m[i]<0):
			invalid=invalid+1
	def ok():
		root.destroy()
	if invalid==0:	
		texto=str("\nTotal numbers of voxels: "+str(max)\
		+"\n \nInvalid voxels (Jacobian determinant < 0): "+str(invalid)+"\n\nThe image registration is valid\n")
	elif invalid!=0:	
		texto=str("\nTotal numbers of voxels: "+str(max)\
		+"\n \nInvalid voxels (Jacobian determinant < 0): "+str(invalid)+"\n\nThe image registration is NOT valid\n")
	
	root = Tk()
	root.geometry('350x160')
	root.title("Image verification")
	var = StringVar()
	label = Message(root, textvariable=var,width=700)
	var.set(texto)
	label.pack()
	root.okButton = tk.Button(root, text='Close',command = ok)
	root.okButton.place(x = 105, y = 0, width=140, height=25)
	root.okButton.pack()
	root.mainloop()
