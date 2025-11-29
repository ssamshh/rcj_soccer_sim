# rcj_soccer_player controller - ROBOT Y1

# Feel free to import built-in libraries
import math  # noqa: F401
import json

# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

robotx , roboty , heading , robot_angle = 0 , 0 , 0 , 0 

data , team_data  , ball_data , heading , direction , robot_pos = "" , "" , "" , "" , "" , ""

zavie_maghsad , error_zavie , error , error_fasele , robot_num , fasele_ta_robot1 , strength1 , robotx1 , roboty1  , state= 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1

data={}

fasele_robot2_ta_robot1=0

to_boro , robot3DataValid  , robot1DataValid  , robot2DataValid = False , False , False , False

robot_num , ballx2 , bally2 , robotx2 , roboty2 , strength2 , ballx1 , bally1 , robotx1 , roboty1 , strength1 = 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0  

class MyRobot3(RCJSoccerRobot):
    
    def send_data(self):

        if utils.ball_is_available==1:

            robot3DataValid=True
            data = {"robot_num": 3,
                    'toop_be_zamin_x':utils.toop_be_zamin_x,
                    'toop_be_zamin_y':utils.toop_be_zamin_y,
                    'robot_x':utils.robotx,
                    'robot_y':utils.roboty,
                    'strength':utils.strength,
                    'to_boro':to_boro,
                    'robot3DataValid':robot3DataValid}
            packet = json.dumps(data)
            self.team_emitter.send(packet)
            
        else:

            robot3DataValid=False
            data = {"robot_num": 3,
                    'robot_x':utils.robotx,
                    'robot_y':utils.roboty,
                    'to_boro':to_boro,
                    'robot3DataValid':robot3DataValid}
            packet = json.dumps(data)
            self.team_emitter.send(packet)

    def receive_data(self): 

        global data , robot_num , to_boro
        global ballx2 , bally2 , robotx2 , roboty2 , strength2 , robot2DataValid
        global robotx1 , roboty1 , strength1 , fasele_ta_robot1 , fasele_robot2_ta_robot1 , ballx1 , bally1 , robot1DataValid
         
        while self.team_receiver.getQueueLength() > 0:
            packet = self.team_receiver.getString()
            self.team_receiver.nextPacket()
            data = json.loads(packet)

            for key, value in data.items():
                if key=='robot_num':
                    robot_num=value
                    # print(f'Robot ID : {robot_num}')
                if robot_num==1:
                    if key=='toop_be_zamin_x':
                        ballx1=value
                        # print(f'Ball X  1 : {ballx1}')
                    elif key=='toop_be_zamin_y':
                        bally1=value
                        # print(f'Ball Y 1 : {bally1}')
                    elif key=='robot_x':
                        robotx1=value
                        # print(f'Robot X 1 : {robotx1}')
                    elif key=='robot_y':
                        roboty1=value
                        # print(f'Robot Y 1 : {roboty1}')
                    elif key=='strength':
                        strength1=value
                        # print(f'Strength ball -> Robot 1 : {strength1}')
                    elif key == "robot1DataValid" :
                        robot1DataValid = value 
                        # print(f'Data Valid Robot1 : {robot1DataValid}')
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
                    elif key=='fasele_ta_robot1':
                        fasele_robot2_ta_robot1=value
                        # print(f'Distance Robot2 -> Robot1 : {fasele_robot2_ta_robot1}')
                    elif key=='robot2DataValid':
                        robot2DataValid=value
                        # print(f'Data Valid Robot 2 : {robot2DataValid}')
                    

    def run(self):

        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)

        while self.robot.step(TIME_STEP) != -1 :

            self.send_data()
            self.receive_data()

            if self.is_new_data():
                global to_boro
                
                utils.sensorUpdates(self)
                utils.toop_be_zamin_update(self)
                fasele_ta_robot1=math.sqrt((robotx1-utils.robotx)**2+(roboty1-utils.roboty)**2)
                

                if utils.ball_is_available==1:
                    utils.turn(self)
                else:
                    utils.go_to(self,0.3,0.4)

                # if fasele_robot2_ta_robot1<fasele_ta_robot1:
                #     to_boro=True
                # else:
                #     to_boro=False
                #     if roboty1>0.69 and 0.23<robotx1<0.35:
                #         utils.go_to(self,0.3,0.71)
                #     elif roboty1>0.69 and -0.23>robotx1>-0.35:
                #         utils.go_to(self,-0.3,0.71)

                self.send_data_to_team(self.player_id)
