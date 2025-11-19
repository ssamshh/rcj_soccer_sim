import math  # noqa: F401
import json
# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

robotx=0 
roboty=0
heading=0
robot_pos=''
robot_angle=0
data = ""
team_data = ""
ball_data = ""
heading = ""
direction = ""
zavie_maghsad=0
error_zavie=0
error=0
error_fasele=0
ballx1 = 0
ballx2 = 0
bally1 = 0
bally2 = 0
Strength1 = 0
Strength2 = 0
RobotX1 = 0
RobotX2 = 0
DistZRobot2 = 0
YouGo = ""
DistRobot1ZRobot2 = 0
YouGo1 = ""

class MyRobot3(RCJSoccerRobot):

    def position(self):
        if utils.ball_is_available == 0:
            utils.go_to(self,-0.37,0.08)

    def SendData(self):
        data = {"robot_id": 3, 
                "ballx" : utils.toop_be_zamin_x ,
                "bally" : utils.toop_be_zamin_y ,
                "robotx" : utils.robotx ,
                "roboty" : utils.roboty ,
                "strength" : utils.strength ,
                "distGoal" : utils.DistZGoal ,
                "DZR2" : DistZRobot2,
                "you_go" : YouGo,
                }
        packet = json.dumps(data)
        self.team_emitter.send(packet)
    
    def ReceiveData(self):
        global data
        global ballx1 
        global ballx2
        global RobotX1
        global RobotX2
        global RobotY1
        global RobotY2
        global Strength1
        global Strength2
        global DistRobot1ZRobot2
        global YouGo1

        while self.team_receiver.getQueueLength() > 0:
            packet = self.team_receiver.getString()
            self.team_receiver.nextPacket()
            data = json.loads(packet)

            for key,value in data.items():
                if key == 'robot_id':
                    robot_id = value
                if robot_id == 1:
                    if key == "ballx":
                        ballx1 = value
                        # print(f"BallXOne : {ballx1}")

                    elif key == "bally":
                        bally1 = value
                        # print(f"BallYOne : {bally1}")

                    elif key == "robotx":
                        RobotX1 = value
                        # print(f"RobotXOne : {RobotX1}")

                    elif key == "roboty":
                        RobotY1 = value
                        # print(f"RobotYOne : {RobotY1}")

                    elif key == "strength":
                        Strength1 = value
                        # print(f'StrengthOne : {Strength1}')

                    elif key == "distGoal" :
                        distGoal1 = value 
                        # print(f'DistGoalOne {distGoal1} ')

                    elif key == "you_go":
                        YouGo1 = value
                        # print(f'YouGo One : {YouGo1}')

                    elif key == "DZR2" :
                        DistRobot1ZRobot2 = value
                        print(f'Distance Robot1 by Robot2 : {DistRobot1ZRobot2}')

                elif robot_id ==  2:
                    if key == "roboty":
                        RobotY2 = value
                        # print(f"RobotYTwo : {RobotY2}")
                    elif key == "robotx":
                        RobotX2 = value
                        # print(f"RobotXTwo : {RobotX2}")    
                    elif key == "bally":
                        bally2 = value
                        # print(f"BallYTwo : {bally2}")
                    elif key == "ballx":
                        ballx2 = value
                        # print(f"BallXTwo : {ballx2}")   
                    elif key == "strength":
                        Strength2 = value
                        # print(f'StrengthTwo : {Strength2}')  
                        
                    elif key == "distGoal" :
                        distGoal2 = value 
                        # print(f'DistGoalTwo {distGoal2} ')
                    

    
    def BehindOFRobot2(self):
        DistZRobot2 = math.sqrt((RobotX2-utils.robotx) ** 2 + (RobotY2 - utils.roboty) ** 2)
        # print(DistZRobot2)
        if DistRobot1ZRobot2 < DistZRobot2:
            YouGo1 = True
        else :
            YouGo1 = False
      
        if YouGo1 == True:
            if RobotY2 > 0.69 and 0.23 < RobotX1 < 0.35 :
                utils.go_to(self,0.3,0.71)
            elif RobotY2 > 0.69 and -0.23 > RobotX2 > -0.35:
                utils.go_to(self,-0.3,0.71)
            else :
                utils.turn2()
        else :
            utils.turn2(self)



    def run(self):
        
       
        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)
        while self.robot.step(TIME_STEP) != -1 :

            self.SendData()
            self.ReceiveData()

            if self.is_new_data():
                utils.toop_be_zamin_update(self)
                utils.sensorUpdates(self)
                if utils.ball_is_available == 0:
                    utils.go_to(self,-0.38,0.08)
                else :       
                    # self.BehindOFRobot2()
                    utils.turn2(self)

                self.send_data_to_team(self.player_id)  