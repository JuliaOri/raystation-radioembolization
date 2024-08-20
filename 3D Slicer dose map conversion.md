# 3D Slicer dose map converison
These are the instructions for map dose conversion using 3D Slicer free software.

##  Download 3D Slicer 
Download and install 3D Slicer at the official download page *https://download.slicer.org/*

You must also install the *SlicerElastix* and the *SlicerRT* modules using the Slicer Extension Manager.

Finally, you must import the CT and NM dicom files.

## Resample the dose map
This will align the CT and dose studies. To do so, open the resample module selecting *"Registration\Resample Image (BRAINS)"*
![resample](https://github.com/user-attachments/assets/90eaede1-743f-4c8d-af0b-293f5312f934)
The input *"Image to Wrap"* must be the map dose file, and the *"Reference Image"* must be the CT file.. Select the *float* pixel type, and *linear* interpolation mode.
