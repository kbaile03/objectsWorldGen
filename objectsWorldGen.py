################################################################################
# Kennedy Bailey                                                               #
# objectsWorldGen.py                                                           #
#                                                                              #
# Generates a world and launch files from user input                           #
#                                                                               #
# Most of this is based on Mar Freeman's blocksWorldGen                        #
#                                                                              #
################################################################################

import os
world = raw_input("Input world name: ")

################################################################################

pr2_launch = "/opt/ros/indigo/share/pr2_gazebo/launch/pr2_%s.launch" % world
f = open(pr2_launch, 'w+')

print >> f, """<launch>

  <!-- start up empty world -->
  <arg name="gui" default="true"/>
  <arg name="paused" default="true"/>
  <!-- TODO: throttled not implemented in gazebo_ros/empty_world.launch
  <arg name="throttled" default="false"/>
  -->

  <include file="$(find gazebo_ros)/launch/%s.launch">
    <!-- TODO: throttled not implemented in gazebo_ros/empty_world.launch
    <arg name="throttled" value="$(arg throttled)" />
    -->
  </include>

  <!-- start pr2 robot -->
  <include file="$(find pr2_gazebo)/launch/pr2.launch"/>

</launch>""" % world

################################################################################

launch = "/opt/ros/indigo/share/gazebo_ros/launch/%s.launch" % world
f = open(launch, 'w+')

print  >> f, """<launch>

  <!-- We resume the logic in empty_world.launch, changing only the name of the world to be launched -->
  <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="world_name" value="worlds/%s.world"/> <!-- Note: the world_name is with respect to GAZEBO_RESOURCE_PATH environmental variable -->
    <arg name="use_sim_time" value="true"/>
    <arg name="headless" value="false"/>
    <arg name="debug" value="false"/>
  </include>

</launch>""" % world

################################################################################

sdf = "/usr/share/gazebo-2.2/worlds/%s.world" % world
f = open(sdf, 'w+')

################################################################################

models = []
print "Choose models from following: (CaseSensitive): "
print(os.listdir("/home/kbailey/.gazebo/models"))

num_objects = 0
model = ""
print("Enter object names separated by newlines (CaseSensitive, type 'done' to end)")
while model != "done":
    model = raw_input("Enter Model: ")
    if model == "done":
        break
    elif not (os.path.exists("/home/kbailey/.gazebo/models/%s" % model)):
        print("Model %s does not exist. Try again" % model)
    else:
        x = raw_input("Enter x: ")
        y = raw_input("Enter y: ")
        z = raw_input("Enter z: ")
        roll = raw_input("Enter roll: ")
        pitch = raw_input("Enter pitch: ")
        yaw = raw_input("Enter yaw: ")

        models.append([])

        models[num_objects].append(model)
        models[num_objects].append(x)
        models[num_objects].append(y)
        models[num_objects].append(z)
        models[num_objects].append(roll)
        models[num_objects].append(pitch)
        models[num_objects].append(yaw)
        num_objects = num_objects + 1


for i in range(0, num_objects):
    print models[i][0]
    print models[i][1]
    print models[i][2]
    print models[i][3]
    print models[i][4]
    print models[i][5]
    print models[i][6]

############################################################################

print >> f, """<?xml version="1.0" ?>
<sdf version="1.4">
  <world name="default">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
    <include>
      <uri>model://short_table2</uri>
      <pose>0.8 0 0 0 0 0</pose>
    </include>
    """

for i in range (num_objects):
    print >> f, """    <include>
      <uri>model://%s</uri>""" % models[i][0]
    print >> f, """      <pose>%s %s %s %s %s %s</pose>
    </include>""" % (models[i][1], models[i][2], models[i][3], models[i][4], models[i][5], models[i][6])

print >> f, """    </world>
  </sdf>"""
