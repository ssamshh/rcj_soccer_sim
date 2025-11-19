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
ballx1 = 0
ballx3 = 0
bally1 = 0
bally3 = 0
Strength1 = 0
Strength3 = 0
RobotX1 = 0
RobotX3 = 0
class MyRobot2(RCJSoccerRobot):
    # def print_sensors(self):
    #     # print(utils.ball_angle)
    #     # print(utils.robot_angle)
    #     print("")


    def run(self):
        global data
        global ballx1 
        global ballx3
        global RobotX1
        global RobotX3
        global RobotY1
        global RobotY3
        global Strength1
        global Strength3
        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)
        while self.robot.step(TIME_STEP) != -1:

            data = { "robot_id" : 2 , 
                    "ballx" : utils.toop_be_zamin_x, 
                    "bally" : utils.toop_be_zamin_y, 
                    "robotx" : utils.robotx,
                    "roboty" : roboty, 
                    "strength" : utils.strength ,
                    "distGoal" : utils.DistZGoal,
                    
                    }

            packet = json.dumps(data)
            self.team_emitter.send(packet)

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
                
                    elif robot_id == 3 :
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

            if self.is_new_data():
                # print_sensors(self)
                utils.sensorUpdates(self)
                utils.toop_be_zamin_update(self)
                utils.goal_keeper(self)
                
                # print('ROBOT X :',utils.toop_be_zamin_x,'ROBOT Y : ',utils.toop_be_zamin_y)
                # print(utils.ball_is_available)
                if utils.ball_is_available == 0:
                    utils.go_to(self,-0.0019,0.58)
                    # if utils.robotx > -0.0019 and utils.roboty < 0.58 :
                    #     if robot_angle > 2:
                    #         utils.move(self, 1, -1)   
                    #     elif robot_angle < -2:
                    #         utils.move(self, -1, 1)  
                    #     else:
                    #         utils.move(self, 0, 0)
                print("1")
                self.send_data_to_team(self.player_id)