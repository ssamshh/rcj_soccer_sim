# rcj_soccer_player controller - ROBOT Y1

# Feel free to import built-in libraries
import math  # noqa: F401
import json

# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

robotx , roboty , heading , robot_angle = 0 , 0 , 0 , 0 

robot_pos , data , team_data , ball_data , heading , direction = '' , '' , '' , '' , '' , ''

zavie_maghsad , error_zavie , error , error_fasele , robot_num , ballx3 = 0 , 0 , 0 , 0 , 0 , 0 

robot3DataValid , robot2DataValid  , robot1DataValid = False , False , False

robot_num , ballx2 , bally2 , robotx2 , roboty2 , strength2 , ballx3 , bally3 , robotx3 , roboty3 , strength3  , state= 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1

othersBallX , othersBallY , numbersOfValidData , othersBallXFinal , othersBallyFinal = 0 , 0 , 0 , 0 , 0 


class MyRobot1(RCJSoccerRobot):
    def send_data(self):

        if utils.ball_is_available == 1 :

            robot1DataValid=True 
            data = {"robot_num": 1,
                    'toop_be_zamin_x':utils.toop_be_zamin_x,
                    'toop_be_zamin_y':utils.toop_be_zamin_y,
                    'robot_x':utils.robotx,
                    'robot_y':utils.roboty,
                    'strength':utils.strength,
                    "robot1DataValid" : robot1DataValid}
            packet = json.dumps(data)
            self.team_emitter.send(packet)
        
        else :
            robot1DataValid=False
            data = {"robot_num": 1,
                    'robot_x':utils.robotx,
                    'robot_y':utils.roboty,
                    "robot1DataValid" : robot1DataValid}
            packet = json.dumps(data)
            self.team_emitter.send(packet)

    def receive_data(self):

        global data , robot_num 
        global ballx2 , bally2 , robotx2 , roboty2 , strength2 , robot2DataValid
        global ballx3 , bally3 , robotx3 , roboty3 , strength3 , robot3DataValid 
       

        while self.team_receiver.getQueueLength() > 0:
            packet = self.team_receiver.getString()
            self.team_receiver.nextPacket()
            data = json.loads(packet)

            for key, value in data.items():
                if key=='robot_num':
                    robot_num=value
                if robot_num==3:
                    # print(f'Robot ID : {robot_num}')
                    if key=='toop_be_zamin_x':
                        ballx3=value
                        # print(f'Ball X  3 : {ballx3}')
                    elif key=='toop_be_zamin_y':
                        bally3=value
                        # print(f'Ball Y 3 : {bally3}')
                    elif key=='robot_x':
                        robotx3=value
                        # print(f'Robot X 3 : {robotx3}')
                    elif key=='robot_y':
                        roboty3=value
                        # print(f'Robot Y 3 : {roboty3}')
                    elif key=='strength':
                        strength3=value
                        # print(f'Strength ball -> Robot 3 : {strength3}')
                    elif key=="robot3DataValid":
                        robot3DataValid=value
                        # print(f'Data Valid Robot 3 : {robot3DataValid}')
                        
                elif robot_num==2:
                    # print(f'Robot ID : {robot_num}')
                    if key=='toop_be_zamin_x':
                        ballx2=value
                        # print(f'Ball X  2 : {ballx2}')
                    elif key=='toop_be_zamin_y':
                        bally2=value
                        # print(f'Ball Y 2 : {bally2}')
                    elif key=='robot_x':
                        robotx2=value
                        # print(f'Robot X 2 : {robotx2}')
                    elif key=='robot_y':
                        roboty2=value
                        # print(f'Robot Y 2 : {roboty2}')
                    elif key=='strength':
                        strength2=value
                        # print(f'Strength ball -> Robot 2 : {strength2}')
                    elif key=='robot2DataValid':
                        robot2DataValid=value
                        # print(f'Data Valid Robot 2 : {robot2DataValid}')

    def GoalKeeper(self):
        global othersBallX , othersBallXFinal
        global othersBallY , othersBallyFinal
        global numbersOfValidData

        if utils.ball_is_available==1:
            utils.goal_keeper(self)
        else:
            
            othersBallX=0
            if robot2DataValid==True:
                othersBallX = ballx2 + othersBallX
                numbersOfValidData+=1
            if robot3DataValid==True:
                othersBallX = ballx3 + othersBallX
                numbersOfValidData+=1
            if numbersOfValidData>0:
                othersBallXFinal= othersBallX / numbersOfValidData
            
            othersBallY=0
            numbersOfValidData=0

            if robot2DataValid==True:
                othersBallY= bally2 + othersBallY
                numbersOfValidData+=1
            if robot3DataValid==True:
                othersBallY = bally3 + othersBallY
                numbersOfValidData+=1
            if numbersOfValidData>0:
                othersBallyFinal= othersBallY / numbersOfValidData


            if othersBallyFinal<roboty:
                if utils.robotx>0 and utils.robotx<0.3 or utils.robotx<0 and utils.robotx>-0.3 :
                    utils.go_to(self,othersBallX,0.6)
                elif utils.robotx>0:
                    utils.go_to(self,0.3,0.6)
                elif utils.robotx<0:
                    utils.go_to(self,-0.3,0.6)
            elif othersBallyFinal>utils.roboty and utils.robotx>0:
                utils.go_to(self,0.3,othersBallyFinal)
            elif othersBallyFinal>utils.roboty and utils.robotx<0:
                utils.go_to(self,-0.3,othersBallyFinal)
            else:
                utils.go_to(self,0,0.58)




    def run(self): 

        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)

        while self.robot.step(TIME_STEP) != -1 :

            self.send_data()
            self.receive_data()

            if self.is_new_data():


                
                utils.sensorUpdates(self)
                utils.toop_be_zamin_update(self)
                self.GoalKeeper()
                

                self.send_data_to_team(self.player_id)
