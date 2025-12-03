import math
import json

robotx , roboty , heading , robot_angle , zavie_maghsad , error_zavie = 0 ,0 , 0 , 0 , 0 , 0 
robot_pos , data , team_data , ball_data , heading , direction = '' , '' , '' , '' , '' , '' 
error , error_fasele , xb , yb , ball_x , ball_y , direction , strength , ball_dist = 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0
toop_be_zamin_x , toop_be_zamin_y , ball_is_available , zavie_toop_be_robot , is_turning , dist_ta_darvaze = 0 , 0 , 0 , 0 , 0 , 0
ASHAR , state = 3 , 1

def get_direction(ball_vector: list) -> int:
    """Get direction to navigate robot to face the ball

    Args:
        ball_vector (list of floats): Current vector of the ball with respect
            to the robot.

    Returns:
        int: 0 = forward, -1 = right, 1 = left
    """
    if -0.13 <= ball_vector[1] <= 0.13:
        return 0
    return -1 if ball_vector[1] < 0 else 1

def move(self, left_speed, right_speed):
    left_speed,right_speed = right_speed,left_speed
    left_speed = min(max(left_speed, -10) , 10)
    right_speed = min(max(right_speed, -10) , 10)
    self.left_motor.setVelocity(left_speed)
    self.right_motor.setVelocity(right_speed)

def sensorUpdates(self):
    global robotx , roboty , robot_pos , data , team_data , ball_data , heading , sonar_values , robot_angle
    global ball_distance , ball_x , ball_y , ball_dist , ball_angle , direction , strength
    global ball_is_available
    global zavie_toop_be_robot , dist_ta_darvaze

    data = self.get_new_data()  

    while self.is_new_team_data():
        team_data = self.get_new_team_data()  
    
    heading = self.get_compass_heading() 
    robot_angle=math.degrees(heading)

    robot_pos = self.get_gps_coordinates()  

    if self.name[0] == "B":
        robotx = robot_pos[0]
        roboty = robot_pos[1]
    else:
        robotx = -robot_pos[0]
        roboty = -robot_pos[1]
    
    sonar_values = self.get_sonar_values()  

    if self.is_new_ball_data():
        ball_is_available=1
        ball_data = self.get_new_ball_data()
        ball_x = ball_data["direction"][0]
        ball_y = ball_data["direction"][1]
        direction = get_direction(ball_data["direction"])
        strength = ball_data["strength"]
    else:
        ball_is_available=0
        ball_data = None
        direction = None

    dist_ta_darvaze=math.sqrt((robotx-0)**2+(roboty-0.7)**2)
    #print(dist_ta_darvaze)

    ball_angle = math.atan2(ball_y, ball_x)
    ball_angle = math.degrees(ball_angle)

    zavie_toop_be_robot=(ball_angle+robot_angle)%360

def go_to(self, x_maghsad, y_maghsad):
    global zavie_maghsad
    global error_zavie , error_fasele , error
    global delta_x , delta_y
    delta_x = x_maghsad - robotx
    delta_y = y_maghsad - roboty
    zavie_maghsad = math.atan2(delta_y, delta_x) * (180 / math.pi)
    zavie_maghsad = (zavie_maghsad - 90)
    if zavie_maghsad < 0:
        zavie_maghsad += 360
    error_zavie = zavie_maghsad - robot_angle
    error_zavie = error_zavie - 180
    if error_zavie > 180:
        error_zavie -= 360
    elif error_zavie < -180:
        error_zavie += 360
    error_zavie = error_zavie * 3
    error_fasele = math.sqrt((delta_x)**2 + (delta_y)**2)
    if error_fasele < 0.5:
        error_fasele = round(error_fasele * 180,3)
    else:
        error_fasele = round(error_fasele * 50,3)
    error = error_zavie
    move(self,error_fasele - error+10, error_fasele + error+10)
    '''if error_fasele>1:
        move(self,error_fasele - error+10, error_fasele + error+10)
    else:
        move(self,0,0)'''

def toop_be_zamin_update(self):

    global last_toop_be_zamin_x ,  last_toop_be_zamin_y , ball_speed , now , delta_time , last_time , ball_angle_predict_deg , newDeg
    global toop_be_zamin_x , toop_be_zamin_y , ball_dist ,  ball_angle , ball_angle_predict , distance 

    r = 0.11886 * ball_dist - 0.02715

    ball_angle = math.atan2(ball_y, ball_x)
    ball_angle = math.degrees(ball_angle)
    if ball_angle < 0:
        ball_angle += 360
    theta = (ball_angle+robot_angle+90) % 360
    if theta < 0:
        theta += 360

    theta = math.radians(theta)
    pos_x = r * math.cos(theta)
    pos_y = r * math.sin(theta)
    pos_x = round(pos_x, ASHAR)
    pos_y = round(pos_y, ASHAR)         
        
    toop_be_zamin_x = robotx + 2.5 * pos_x
    toop_be_zamin_y = roboty + 2.5 * pos_y
    toop_be_zamin_x = round(toop_be_zamin_x, ASHAR)
    toop_be_zamin_y = round(toop_be_zamin_y, ASHAR)

def goal_keeper(self):

    if toop_be_zamin_y<roboty:
        if robotx>0 and robotx<0.3 or robotx<0 and robotx>-0.3 :
            go_to(self,toop_be_zamin_x,0.6)
        elif robotx>0:
            go_to(self,0.3,0.6)
        elif robotx<0:
            go_to(self,-0.3,0.6)
    elif toop_be_zamin_y>roboty and robotx>0:
        go_to(self,0.3,toop_be_zamin_y)
    elif toop_be_zamin_y>roboty and robotx<0:
        go_to(self,-0.3,toop_be_zamin_y)

def goToTheta(self,moveTheta):
    go_to(self,robotx+math.cos(moveTheta*0.0174532925199433)*0.05,roboty+math.sin(moveTheta*0.0174532925199433)*0.05)

def turn(self):
    global is_turning
    if toop_be_zamin_y>roboty:
        is_turning=1
    elif zavie_toop_be_robot>350 or zavie_toop_be_robot<10:
        is_turning=0

    if is_turning==0 and toop_be_zamin_y<0.5:
        if 330>zavie_toop_be_robot>30:
            goToTheta(self,zavie_toop_be_robot-90)
        else:
            if strength>100:
                go_to(self,0,-0.6)
            else:
                goToTheta(self,zavie_toop_be_robot-90)

    elif is_turning==1 and toop_be_zamin_y<0.5:
        if toop_be_zamin_x<robotx:
            goToTheta(self,zavie_toop_be_robot-90 - strength/1.5)
        else: 
            goToTheta(self,zavie_toop_be_robot-90 + strength/1.5)
    elif roboty>0.5:
        go_to(self,0,0.2)

def turn2(self):
    global state
    if toop_be_zamin_y<roboty:
        if state==1:
            go_to(self,toop_be_zamin_x,toop_be_zamin_y+0.045)
            if abs(toop_be_zamin_x-robotx)<0.01 and abs((toop_be_zamin_y+0.045)-roboty)<0.01:
                state=2
        elif state==2:
            go_to(self,toop_be_zamin_x,toop_be_zamin_y)
            if abs(toop_be_zamin_x-robotx)>0.2 and abs(toop_be_zamin_y-roboty)>0.2:
                state=1
    else:
        if toop_be_zamin_x>0 and is_turning==1:
            go_to(self,toop_be_zamin_x-0.05,toop_be_zamin_y+0.045)
        elif toop_be_zamin_x<0 and is_turning==1:
            go_to(self,toop_be_zamin_x+0.05,toop_be_zamin_y+0.045)
 
