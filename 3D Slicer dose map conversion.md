# 3D Slicer dose map converison
These are the instructions for map dose conversion using 3D Slicer free software.

##  Download 3D Slicer 
Download and install 3D Slicer at the official download page *https://download.slicer.org/*

You must also install the *SlicerElastix* and the *SlicerRT* modules using the Slicer Extension Manager.

Finally, you must import the CT and NM dicom files.

### Resample the dose map
This will align the CT and dose studies. To do so, open the resample module selecting *"Registration\Resample Image (BRAINS)"*

![resample](https://github.com/user-attachments/assets/90eaede1-743f-4c8d-af0b-293f5312f934)

The input *"Image to Wrap"* must be the map dose file, and the *"Reference Image"* must be the CT file. Select the *float* pixel type, and *linear* interpolation mode.

![image](https://github.com/user-attachments/assets/78099763-265f-4540-aeb7-3033d18d5064)

To avoid issues when handling very large values, it is also good practice to rescale the *Resample dose map* file with the *"Filtering\Simple filters\ShiftScaleImageFilter"*.

![image](https://github.com/user-attachments/assets/476a2f5a-c587-4254-917d-b1eaee3ad1b9)


### Convert the dose map to RT dose volume
Click on the rescaled dose map and convert it to RT dose volume

![image](https://github.com/user-attachments/assets/26d9dd74-5d39-4480-95de-beef0987a0a2)

Enter the same dose unit value used to resize the image

![image](https://github.com/user-attachments/assets/23071928-d354-476c-a515-604e909fa1a0)

## Export the file
The study is ready to export by clicking *"Export to DICOM..."* with the *"Scalar Volume"* option

![image](https://github.com/user-attachments/assets/3f11a5de-6d7a-424d-a139-7f236ceb9803)


![image](https://github.com/user-attachments/assets/09475e05-7709-4009-b7b5-5576f4edf0a4)
