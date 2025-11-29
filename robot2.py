# rcj_soccer_player controller - ROBOT Y1

# Feel free to import built-in libraries
import math  # noqa: F401
import json

# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

robotx , roboty , heading , robot_angle = 0 , 0 , 0 , 0

data , team_data , ball_data , heading , direction  , robot_pos = "" ,"" ,"" ,"" ,"" , ""

zavie_maghsad , error_zavie , error , error_fasele , is_turning , robot_num , strength1 , robotx1 , roboty1 , fasele_ta_robot1 , state = 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0  

data={}

to_boro , robot2DataValid , robot1DataValid , robot3DataValid= False , False , False , False

robot_num , ballx1 , bally1 , robotx1 , roboty1 , strength1 , ballx3 , bally3 , robotx3 , roboty3 , strength3 = 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 

class MyRobot2(RCJSoccerRobot):

    def send_data(self):

        if utils.ball_is_available==1:
            
            robot2DataValid=True 
            data = {"robot_num":2,
                    'toop_be_zamin_x':utils.toop_be_zamin_x,
                    'toop_be_zamin_y':utils.toop_be_zamin_y,
                    'robot_x':utils.robotx,
                    'robot_y':utils.roboty,
                    'strength':utils.strength,
                    'fasele_ta_robot1':fasele_ta_robot1,
                    'robot2DataValid':robot2DataValid}
            packet = json.dumps(data)
            self.team_emitter.send(packet)

        else:

            robot2DataValid=False
            data = {"robot_num":2,
                    'robot_x':utils.robotx,
                    'robot_y':utils.roboty,
                    'fasele_ta_robot1':fasele_ta_robot1,
                    'robot2DataValid':robot2DataValid}
            packet = json.dumps(data)
            self.team_emitter.send(packet)



    def receive_data(self):

        global robot_num
        global robotx1 , roboty1 , strength1 , data , fasele_ta_robot1 , ballx1 , bally1 , robot1DataValid
        global robotx3 , roboty3 , strength3 , ballx3 , bally3 , to_boro , robot3DataValid

        while self.team_receiver.getQueueLength() > 0:
            packet = self.team_receiver.getString()
            self.team_receiver.nextPacket()
            data = json.loads(packet)

            for key, values in data.items():
                if key=='robot_num':
                    robot_num=values
                if robot_num==1:
                    # print(f'Robot ID : {robot_num}')
                    if key=='toop_be_zamin_x':
                        ballx1=values
                        # print(f'Ball X  1 : {ballx1}')
                    elif key=='toop_be_zamin_y':
                        bally1=values
                        # print(f'Ball Y 1 : {bally1}')
                    elif key=='robot_x':
                        robotx1=values
                        # print(f'Robot X 1 : {robotx1}')
                    elif key=='robot_y':
                        roboty1=values
                        # print(f'Robot Y 1 : {roboty1}')
                    elif key=='strength':
                        strength1=values
                        # print(f'Strength ball -> Robot 1 : {strength1}')
                    elif key == "robot1DataValid" :
                        robot1DataValid = values 
                        # print(f'Data Valid Robot1 : {robot1DataValid}')
                elif robot_num==3:
                    # print(f'Robot ID : {robot_num}')
                    if key=='toop_be_zamin_x':
                        ballx3=values
                        # print(f'Ball X  3 : {ballx3}')
                    elif key=='toop_be_zamin_y':
                        bally3=values
                        # print(f'Ball Y 3 : {bally3}')
                    elif key=='robot_x':
                        robotx3=values
                        # print(f'Robot X 3 : {robotx3}')
                    elif key=='robot_y':
                        roboty3=values
                        # print(f'Robot Y 3 : {roboty3}')
                    elif key=='strength':
                        strength3=values
                        # print(f'Strength ball -> Robot 3 : {strength3}')
                    elif key=='to_boro':
                        to_boro=values
                        # print(f'You Go : {to_boro}')
                    elif key=="robot3DataValid":
                        robot3DataValid=values
                        # print(f'Data Valid Robot 3 : {robot3DataValid}')
                

    def run(self):
 
        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)

        while self.robot.step(TIME_STEP) != -1 :

            self.send_data()
            self.receive_data()

            if self.is_new_data():            
                global fasele_ta_robot1

                utils.sensorUpdates(self) 
                utils.toop_be_zamin_update(self)

                fasele_ta_robot1=math.sqrt((robotx1-utils.robotx)**2+(roboty1-utils.roboty)**2)
                if utils.ball_is_available == 0:
                    utils.go_to(self,-0.3,0.4)
                else :
                    utils.turn2(self)



                # if to_boro==True:
                #     if roboty1>0.69 and 0.23<robotx1<0.35:
                #         utils.go_to(self,0.3,0.71)
                #     elif roboty1>0.69 and -0.23>robotx1>-0.35:
                #         utils.go_to(self,-0.3,0.71)
                #     else:
                #         utils.turn(self)
                

                self.send_data_to_team(self.player_id)
