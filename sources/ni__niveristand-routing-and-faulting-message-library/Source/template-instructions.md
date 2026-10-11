# Create a New Messaging Library

1. Copy the "Template" Folder into the Source Folder.

2. Rename the folder the name of your device to add.

3. Open the %DEVICE% Messaging project.

4. Rename the Project.

5. Rename the Mock Consumer Class at My Computer/Tests/Support.

6. Rename the Messaging Tests Class at My Computer/Tests.

7. For each Target:
    
    a. Rename the Messaging Library at My Computer.

    b. Open the build spec, and rename the Build specification.
    
    c. Change the Target filename to your device name with no spaces.

# Implement Message Classes

1. Open the switch messaging library outside of the project.

2. In the Consumer class, open private/Session Type.ctl and replace it with your device's session handle type.

3. Open the Bookmark Manager, and modify the VIs listed there to match your device's API.