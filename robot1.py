import math  
import json
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
ballx2 = 0
ballx3 = 0
bally2 = 0
bally3 = 0
Strength2 = 0
Strength3 = 0
RobotX2 = 0
RobotX3 = 0
RobotY3 = 0
RobotY2 = 0
DistZRobot2 = 0
YouGo = False
RobotX1 = 0

class MyRobot1(RCJSoccerRobot):
    def SendData(self):
        data = {"robot_id": 1, 
                "ballx" : utils.toop_be_zamin_x ,
                "bally" : utils.toop_be_zamin_y ,
                "robotx" : utils.robotx ,
                "roboty" : utils.roboty ,
                "strength" : utils.strength ,
                "distGoal" : utils.DistZGoal ,
                "DistZRobot2" : DistZRobot2,
                "DZR2 " : DistZRobot2
                }
        packet = json.dumps(data)
        self.team_emitter.send(packet)
    def ReceiveData(self):
        global data
        global ballx2
        global ballx3
        global RobotX2
        global RobotX3
        global RobotY2
        global RobotY3
        global Strength2
        global Strength3
        global DistRobot3ZRobot2
        global YouGo

        while self.team_receiver.getQueueLength() > 0:
            packet = self.team_receiver.getString()
            self.team_receiver.nextPacket()
            data = json.loads(packet)

            for key,value in data.items():
                if key == 'robot_id':
                    robot_id = value
                if robot_id == 2:
                    if key == "ballx":
                        ballx2 = value
                        # print(f"BallXTwo : {ballx2}")

                    elif key == "bally":
                        bally2 = value
                        # print(f"BallYTwo : {bally2}")

                    elif key == "robotx":
                        RobotX2 = value
                        # print(f"RobotXTwo  : {RobotX2}")

                    elif key == "roboty":
                        RobotY2 = value
                        # print(f"RobotYTwo  : {RobotY2}")
                
                    elif key == "strength":
                        Strength2 = value
                        # print(f'StrengthTwo  : {Strength2}')
                        
                    elif key == "distGoal" :
                        distGoal2 = value 
                        # print(f'DistGoalTwo {distGoal2} ')   
                    



                elif robot_id == 3:
                    if key == "strength":
                        Strength3 = value
                        # print(f'StrengthThree : {Strength3}')

                    elif key == "roboty":
                        RobotY3 = value
                        # print(f"RobotYThree : {RobotY3}")

                    elif key == "robotx":
                        RobotX3 = value
                        # print(f"RobotXThree : {RobotX3}")

                    elif key == "bally":
                        bally3 = value
                        # print(f"BallYThree : {bally3}") 

                    elif key == "ballx":
                        ballx3 = value
                        # print(f"BallXThree : {ballx3}")

                    elif key == "distGoal" :
                        distGoal3 = value 
                        # print(f'DistGoalThree {distGoal3} ') 

                    elif key == "you_go":
                        YouGo = value
                        print(f'YouGo Three {YouGo}')

    
    def BehindOFRobot2(self):
        DistZRobot2 = math.sqrt((RobotX2-utils.robotx) ** 2 + (RobotY2 - utils.roboty) ** 2)
        if YouGo == True:
            if RobotY2 > 0.69 and 0.23 < RobotX1 < 0.35 :
                utils.go_to(self,0.3,0.71)
                print('situation one')
            elif RobotY2 > 0.69 and -0.23 > RobotX2 > -0.35:
                utils.go_to(self,-0.3,0.71)
                print('situation Two')
            else :
                utils.turn2(self)
                print('situation three')
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
                    utils.go_to(self,0.37,0.08)
                else :
                    # utils.turn2(self)
                    self.BehindOFRobot2()


                self.send_data_to_team(self.player_id)   
