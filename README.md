# v1.0.0
## GOAL - get informations from the server and display it with the client

### Client UI:
###### main page:
    - connects to the server and shows the infos in tabs
    - arrow movement: side is tab change horizontal is line change
###### tabs:
    - general information
        - platfrom, hostname etc.
    - system stats
        - cpu: overall stats
        - memory: overall stats, virtual mem only
    - disk:
        - all partitions listed: name, device, mountpoint, type, usage

### Client Backend:
    - based on the selected tab, ask server for that type of info wiht the delaytime from the settings

### Server:
###### on call:
    - check call type and get/return the selected informations

### Communication format:
###### data types for each tab:
    - general : for the information tab
    - system : for the system stats
    - disk : for the disk data
