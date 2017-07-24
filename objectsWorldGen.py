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


num_objects = input("Input the number of objects you plan to spawn: ")


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
print(os.listdir("/Users/Kennedy/Desktop/test"))

num_objects = 0

model = ""
print("Enter object names separated by newlines (CaseSensitive, type 'done' to end)")
while model != "done":
    model = raw_input("Enter Model: ")
    if model == "done":
        break
    elif not (os.path.exists("/Users/Kennedy/Desktop/test/%s" % model)):
        print("Model %s does not exist. Try again" % model)
    else:
        x = raw_input("Enter x: ")
        y = raw_input("Enter y: ")
        z = raw_input("Enter z: ")

        models.append([])

        models[num_objects].append(model)
        models[num_objects].append(x)
        models[num_objects].append(y)
        models[num_objects].append(z)

        num_objects = num_objects + 1

################################################################################

table_dist = 0.7
table_height = -0.1
model = ""

print >> f, """<?xml version="1.0" ?>
<sdf version="1.4">
  <world name="default">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>"""
    
for i in range (num_blocks):
    print >> f, "    <model name='unit_box_%d'>" % i
    blocks[i][x] = -(2.0*blocks[i][x]-1.0)*0.0254 + table_dist
    blocks[i][y] = (2.0*blocks[i][y]-1.0)*0.0254
    blocks[i][z] = (2.0*blocks[i][z]-1.0)*0.0254 + table_height + 0.82
    print blocks[i]
    print >> f, "      <pose>%f %f %f 0 0 0</pose>" % (blocks[i][x], blocks[i][y], blocks[i][z])
    print >> f, """      <link name="link">
        <inertial>
          <mass>0.0943</mass>
          <inertia>
            <ixx>4.056e-5</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>4.056e-5</iyy>
            <iyz>0</iyz>
            <izz>4.056e-5</izz>
          </inertia>
        </inertial>
        <collision name="collision">
          <geometry>
            <box>
              <size>0.0508 0.0508 0.0508</size>
            </box>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>0.3</mu>
                <mu2>0.3</mu2>
              </ode>
            </friction>
            <contact>
              <ode>
                <min_depth>0.001</min_depth>
                <kd>1.0</kd>
                <kp>100000</kp>
              </ode>
            </contact>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.0508 0.0508 0.0508</size>
            </box>
          </geometry>
          <material>
            <script>
              <uri>file://media/materials/scripts/gazebo.material</uri>
              <name>Gazebo/%s</name>
            </script>
          </material>
        </visual>
      </link>
    </model>""" % blocks[i][color]

print >> f, """    <model name='cafe_table'>
      <static>1</static>
      <link name='link'>
        <collision name='surface'>
          <pose>0 0 0.755 0 -0 0</pose>
          <geometry>
            <box>
              <size>0.913 0.913 0.04</size>
            </box>
          </geometry>
          <max_contacts>10</max_contacts>
          <surface>
            <bounce/>
            <friction>
              <ode/>
            </friction>
            <contact>
              <ode/>
            </contact>
          </surface>
        </collision>
        <collision name='column'>
          <pose>0 0 0.37 0 -0 0</pose>
          <geometry>
            <box>
              <size>0.042 0.042 0.74</size>
            </box>
          </geometry>
          <max_contacts>10</max_contacts>
          <surface>
            <bounce/>
            <friction>
              <ode/>
            </friction>
            <contact>
              <ode/>
            </contact>
          </surface>
        </collision>
        <collision name='base'>
          <pose>0 0 0.02 0 -0 0</pose>
          <geometry>
            <box>
              <size>0.56 0.56 0.04</size>
            </box>
          </geometry>
          <max_contacts>10</max_contacts>
          <surface>
            <bounce/>
            <friction>
              <ode/>
            </friction>
            <contact>
              <ode/>
            </contact>
          </surface>
        </collision>
        <visual name='visual'>
          <geometry>
            <mesh>
              <uri>model://cafe_table/meshes/cafe_table.dae</uri>
            </mesh>
          </geometry>
        </visual>
        <velocity_decay>
          <linear>0</linear>
          <angular>0</angular>
        </velocity_decay>
        <self_collide>0</self_collide>
        <kinematic>0</kinematic>
        <gravity>1</gravity>
      </link>
      <pose>%f 0 %f 0 -0 0</pose>
    </model>
  </world>
</sdf>""" % (table_dist, table_height)
