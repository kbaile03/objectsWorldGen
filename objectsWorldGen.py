################################################################################
# Kennedy Bailey                                                               #
# objectsWorldGen.py                                                           #
#                                                                              #
# Generates a world and launch files from user input                           #
#                                                                              #
# Most of this is based on Mar Freeman's blocksWorldGen                        #
#                                                                              #
################################################################################

import os
import sys

config = ""
home_path = os.getenv("HOME")

print "Home path: '%s'" %home_path

if (not(os.path.isdir("%s/.gazebo/models" %home_path))):
    print "Gazebo models path set incorrectly. Exiting"
    sys.exit()

while (config != "Tabletop" and config != "Absolute"):
    config = raw_input("Choose configuration ('Tabletop' or 'Absolute'): ")
    print "Entered: %s" %config

world = raw_input("Input world name: ")

################################################################################
################################### UNIVERSAL ##################################
################################################################################

pr2_launch = "/opt/ros/indigo/share/pr2_gazebo/launch/pr2_%s.launch" %world
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
  <include file="$(find pr2_moveit_config)/launch/move_group.launch"/>

</launch>""" %world

################################################################################

launch = "/opt/ros/indigo/share/gazebo_ros/launch/%s.launch" %world
f = open(launch, 'w+')

print  >> f, """<launch>

  <!-- We resume the logic in empty_world.launch, changing only the name of the world to be launched -->
  <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="world_name" value="worlds/%s.world"/> <!-- Note: the world_name is with respect to GAZEBO_RESOURCE_PATH environmental variable -->
    <arg name="use_sim_time" value="true"/>
    <arg name="headless" value="false"/>
    <arg name="debug" value="false"/>
  </include>

</launch>""" %world

################################################################################

sdf = "/usr/share/gazebo-2.2/worlds/%s.world" %world
f = open(sdf, 'w+')

models = []
num_objects = 0
model = ""

################################################################################
################################### ABSOLUTE ###################################
################################################################################

if config == "Absolute":
    print("Enter object names separated by newlines (CaseSensitive, type 'done' to end)")
    while model != "done":
        print "Choose models from following: (CaseSensitive): "
        print(os.listdir("%s/.gazebo/models" %home_path))
        model = raw_input("Enter Model or type 'done': ")
        if model == "done":
            break
        elif not (os.path.exists("%s/.gazebo/models/%s" %(home_path, model))):
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

################################################################################
    print >> f, """<?xml version="1.0" ?>
  <sdf version="1.4">
    <world name="%s_world">
      <include>
        <uri>model://ground_plane</uri>
      </include>
      <include>
        <uri>model://sun</uri>
      </include>
      """ %world

    for i in range (num_objects):
        print >> f, """       <include>
        <uri>model://%s</uri>
        <name>%s</name>""" %(models[i][0], models[i][0])
        print >> f, """        <pose>%s %s %s %s %s %s</pose>
      </include>""" % (models[i][1], models[i][2], models[i][3], models[i][4], models[i][5], models[i][6])

    print >> f, """    </world>
  </sdf>"""

################################################################################
################################## TABLETOP ####################################
################################################################################

elif config == "Tabletop":
    table_height = float(raw_input("Enter table height in meters: ")) + -0.6
    print("Enter object names and dimensions separated by newlines (CaseSensitive, type 'done' to end)")
    while model != "done":
        print "Choose models from following: (CaseSensitive): "
        print(os.listdir("%s/.gazebo/models" %home_path))
        model = raw_input("Enter Model or type 'done': ")
        if model == "done":
            break
        elif not (os.path.exists("%s/.gazebo/models/%s" %(home_path, model))):
            print("Model %s does not exist. Try again" %model)
        else:
            print """

   -3.0  -2.5  -2.0  -1.5  -1.0  -0.5   0.0   0.5   1.0   1.5   2.0   2.5   3.0 x
2.0  +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
     |     |     |     |     |     |     |     |     |     |     |     |     |
1.5 _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|
     |     |     |     |     |     |     |     |     |     |     |     |     |
     |     |     |     |     |     |     |     |     |     |     |     |     |
1.0  +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
     |     |     |     |     |     |     |     |     |     |     |     |     |
0.5 _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|
     |     |     |     |     |     |     |     |     |     |     |     |     |
     |     |     |     |     |     |     |     |     |     |     |     |     |
0.0  +-----+-----+-----+-----+----T+A-B-L+E-T-O+P----+-----+-----+-----+-----+
     |     |     |     |     |     |     |     |     |     |     |     |     |
-0.5_|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|
     |     |     |     |     |     |     |     |     |     |     |     |     |
     |     |     |     |     |     |     |     |     |     |     |     |     |
-1.0 +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
     |     |     |     |     |     |     |     |     |     |     |     |     |
-1.5_|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|_ _ _|
     |     |     |     |     |     |     |     |     |     |     |     |     |
     |     |     |     |     |     |     |     |     |     |     |     |     |
-2.0 +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
  y
"""
            x = float(raw_input("Enter x: "))/5
            y = float(raw_input("Enter y: "))/4 + 0.8

            models.append([])

            models[num_objects].append(model)
            models[num_objects].append(x)
            models[num_objects].append(y)

            print "Added object '%s' at (%f, %f)" %(model, x, y)

            num_objects = num_objects + 1

################################################################################

    print >> f, """<?xml version="1.0" ?>
  <sdf version="1.4">
    <world name="%s_world">
      <include>
        <uri>model://ground_plane</uri>
      </include>
      <include>
        <uri>model://sun</uri>
      </include>
      <include>
        <uri>model://short_table2</uri>
        <name>short_table2</name>
        <pose>0.8 0 %f 0 0 0</pose>
      </include>""" % (world, table_height)

    for i in range (num_objects):
        print >> f, """      <include>
        <uri>model://%s</uri>
        <name>%s</name>""" %(models[i][0], models[i][0])
        print >> f, """        <pose>%f %f %f 0 0 0</pose>
      </include>""" % (models[i][2], models[i][1], table_height + .61)

    print >> f, """    </world>
  </sdf>"""
