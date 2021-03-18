# facerec-api


## ROUTES 


1. Add Group 
```
param :
groupname = name of group
'/addGroup', methods=['POST']
```

2. Add Subgroup
```param :
subgroupname = name of subgroup
groupid = id of father group
'/addSubgroup', methods=['POST']
```

3. Signup new user
```
param 
userid = username
role = role of user (user or superuser)
'/signup', methods=['POST']
```

4. Enter subgroup
```
enters a user to a subgroup, 1 to 1
param :
id = id of user
subgroup = id of subgroup
'/entersubgroup', methods=['POST']
```

5. Enroll
```
enroll an image of a name to a certain subgroup
GUNAKAN form-data
param :
userid = username yang sedang memakai, akan dicek superuser atau bukan
name = nama pemilik wajah
imagefile (type : image) = file image wajah
subgroupid = id subgroup target
'/enroll', methods=['POST']
```

6. Recognize
```
GUNAKAN form-data
param :
imagefile (type image) = file wajah yang ingin di recognize
target subgroupid = subgroup target
'/recognize',methods=['POST']
```


# CARA NGERUN

## run app.py, harusnya keliatan di port berapa dia jalan
