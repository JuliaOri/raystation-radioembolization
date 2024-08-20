from connect import *
import warnings
from tkinter import *
import tkinter as tk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.simpledialog

case=get_current('Case')
case.TreatmentPlans['SPECT Scaled'].TreatmentCourse.TotalDose.UpdateDoseGridStructures()
#case.TreatmentPlans['PET Scaled'].TreatmentCourse.TotalDose.UpdateDoseGridStructures()
plan=case.TreatmentPlans['SPECT Scaled']
# Utiliza el plan del estudio de referencia, donde se han guardado todas las ROI, independientemente de la dosis que hayan utilizado
plan_dose = plan.TreatmentCourse.TotalDose


def copy(event):
    sel = tree.selection() # get selected items
    root.clipboard_clear()  # clear clipboard
    # copy headers
    headings = [tree.heading("#{}".format(i), "text") for i in range(len(tree.cget("columns")) + 1)]
    root.clipboard_append("\t".join(headings) + "\n")
    for item in sel:
        # retrieve the values of the row
        values = [tree.item(item, 'text')]
        values.extend(tree.item(item, 'values'))
        # append the values separated by \t to the clipboard
        root.clipboard_append("\t".join(values) + "\n")



root = tk.Tk()
root.title('Results (copy to clipboard wih Ctrl + A and Ctrl + C)')
tree = ttk.Treeview(root)
tree.bind('<Control-a>', lambda *args: tree.selection_add(tree.get_children())) #selected all row treeview
tree.bind('<Control-c>', copy)

tree['columns'] = ('10', '20', '30','40','50','60','70','80','90')
tree.column('#0', width=350, stretch=tk.NO)
tree.column('10', width=100, stretch=tk.NO)
tree.column('20', width=100, stretch=tk.NO)
tree.column('30', width=100, stretch=tk.NO)
tree.column('40', width=100, stretch=tk.NO)
tree.column('50', width=100, stretch=tk.NO)
tree.column('60', width=100, stretch=tk.NO)
tree.column('70', width=100, stretch=tk.NO)
tree.column('80', width=100, stretch=tk.NO)
tree.column('90', width=100, stretch=tk.NO)

tree.heading('#0', text='Nominal dose threshold (% max.)', anchor=tk.W)
tree.heading('10', text='10', anchor=tk.W)
tree.heading('20', text='20', anchor=tk.W)
tree.heading('30', text='30', anchor=tk.W)
tree.heading('40', text='40', anchor=tk.W)
tree.heading('50', text='50', anchor=tk.W)
tree.heading('60', text='60', anchor=tk.W)
tree.heading('70', text='70', anchor=tk.W)
tree.heading('80', text='80', anchor=tk.W)
tree.heading('90', text='90', anchor=tk.W)


initial=10
final=100
step=10

with CompositeAction('SPECT ROIs'):
	#SPECT
	volv=tuple()
	av_dosev=tuple()
	for j in range(initial,final,step):
	
		try:#para que ignore los errores si hay algún valor vacío (especialmente si no existe coiincidencia entre la ROI prescrita y la administrada)
			
			c=str(j)+'S'
			# Valor del volumen redondeando al segundo decimal
			vol_val=str(round(plan.BeamSets[0].GetStructureSet().RoiGeometries[c].GetRoiVolume(),2))
			volv=volv+(vol_val,)
			dose=str(round(plan_dose.GetDoseStatistic(RoiName=c, DoseType="Average")/100,2))
			# Recuerda que hay que dividirlo entre 100 porque las odis que maneja multiplican por 100 el valor del voxel
			av_dosev=av_dosev+(dose,)
		
		
		except:#para que ignore los errores si hay algún valor vacío (especialmente si no existe coincidencia entre la ROI prescrita y la administrada)
			volv=volv+("-",)
			av_dosev=av_dosev+("-",)
	tree.insert('', 'end', text='Pre-treatment (SPECT) volume (cc)',values=volv)
	tree.insert('', 'end', text='Pre-treatment (SPECT) volume average dose (% max.)',values=av_dosev)

with CompositeAction('PET ROIs'):
	volv=tuple()
	av_dosev=tuple()
	for j in range(initial,final,step):
		
		try:#para que ignore los errores si hay algún valor vacío (especialmente si no existe coiincidencia entre la ROI prescrita y la administrada)
		
			c=str(j)+'P'
			# Valor del volumen redondeando al segundo decimal
			vol_val=str(round(plan.BeamSets[0].GetStructureSet().RoiGeometries[c].GetRoiVolume(),2))
			volv=volv+(vol_val,)
			dose=str(round(plan_dose.GetDoseStatistic(RoiName=c, DoseType="Average")/100,2))
			# Recuerda que hay que dividirlo entre 100 porque las odis que maneja multiplican por 100 el valor del voxel
			av_dosev=av_dosev+(dose,)
		
		
		except:#para que ignore los errores si hay algún valor vacío (especialmente si no existe coincidencia entre la ROI prescrita y la administrada)
			volv=volv+("-",)
			av_dosev=av_dosev+("-",)
	tree.insert('', 'end', text='Post-treatment (PET) volume (cc)',values=volv)
	tree.insert('', 'end', text='Post-treatment (PET) average dose (% max.)',values=av_dosev)

with CompositeAction('ROIs en las que coincide la dosis prescrita y la administrada'):
	volv=tuple()
	av_dosev=tuple()
	for j in range(initial,final,step):
		
		try:#para que ignore los errores si hay algún valor vacío (especialmente si no existe coiincidencia entre la ROI prescrita y la administrada)
		
			c=str(j)+str(" pres.")
			# Valor del volumen redondeando al segundo decimal
			vol_val=str(round(plan.BeamSets[0].GetStructureSet().RoiGeometries[c].GetRoiVolume(),2))
			volv=volv+(vol_val,)
			dose=str(round(plan_dose.GetDoseStatistic(RoiName=c, DoseType="Average")/100,2))
			# Recuerda que hay que dividirlo entre 100 porque las odis que maneja multiplican por 100 el valor del voxel
			av_dosev=av_dosev+(dose,)
			
		
		except:#para que ignore los errores si hay algún valor vacío (especialmente si no existe coincidencia entre la ROI prescrita y la administrada)
			volv=volv+("-",)
			av_dosev=av_dosev+("-",)
	tree.insert('', 'end', text='Overlapping pre- and post-treatment volume (cc)',values=volv)
	tree.insert('', 'end', text='Overlapping pre- and post-treatment average dose (% max.)',values=av_dosev)

with CompositeAction('Non-prescribed administered ROIs'):
	volv=tuple()
	av_dosev=tuple()
	for j in range(initial,final,step):
		try:#para que ignore los errores si hay algún valor vacío (especialmente si no existe coiincidencia entre la ROI prescrita y la administrada)
		
			c=str(str(j)+" non pres.")
			# Valor del volumen redondeando al segundo decimal
			vol_val=str(round(plan.BeamSets[0].GetStructureSet().RoiGeometries[c].GetRoiVolume(),2))
			volv=volv+(vol_val,)
			dose=str(round(plan_dose.GetDoseStatistic(RoiName=c, DoseType="Average")/100,2))
			# Recuerda que hay que dividirlo entre 100 porque las odis que maneja multiplican por 100 el valor del voxel
			av_dosev=av_dosev+(dose,)
		
		
		except:#para que ignore los errores si hay algún valor vacío (especialmente si no existe coincidencia entre la ROI prescrita y la administrada)
			volv=volv+("-",)
			av_dosev=av_dosev+("-",)
	tree.insert('', 'end', text='Non-overlapping volume (cc)',values=volv)
	tree.insert('', 'end', text='Non-overlapping average dose (% max.)',values=av_dosev)


def callback(binding):
    print('Callback from:', binding)

tree.bind('<Control-A>', lambda *args: tree.selection_add(tree.get_children())) #selected all row treeview
tree.bind('<Control-C>', copy)
tree.bind('<Control-a>', lambda *args: tree.selection_add(tree.get_children())) #selected all row treeview
tree.bind('<Control-c>', copy)
tree.pack()
root.mainloop()
