import math

robotx=0 
roboty=0
heading=0
robot_pos=''
robot_angle=0
data = ""
team_data = ""
ball_data = 0
heading = ""
direction = 0
zavie_maghsad=0
error_zavie=0
error=0
error_fasele=0
xb=0
yb=0
ball_x=0
ball_y=0
direction=0
strength=0
ball_dist=0
ASHAR=3
toop_be_zamin_x=0
toop_be_zamin_y=0
ball_angle_predict = 0
distance = 0
ball_speed = 0
delta_time = 0
last_time = 0
ball_angle_predict_deg = 0
newDeg = 0
ball_x = 0 
ball_y = 0  
strength = 0  
ball_angle = 0
sfront = 0
sright = 0
sback = 0
sleft = 0
state = 1
ball_is_available = 0
deg_ball_by_robot = 0
is_turning = 0
DistZGoal = 0
def get_direction(ball_vector: list) -> int:

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
    global robotx
    global roboty
    global robot_pos
    global data
    global team_data
    global ball_data
    global heading
    global sonar_values
    global robot_angle
    global ball_distance
    global ball_x
    global ball_y
    global ball_dist
    global ball_angle
    global direction
    global strength
    global sright 
    global sfront
    global sback
    global sleft
    global deg_ball_by_robot
    global ball_is_available
    global DistZGoal

    data = self.get_new_data()  

    while self.is_new_team_data():
        team_data = self.get_new_team_data()  
    
    heading = self.get_compass_heading() 
    robot_angle=math.degrees(heading)

    robot_pos = self.get_gps_coordinates()  
    robotx=robot_pos[0]
    roboty=robot_pos[1]
    
    sonar_values = self.get_sonar_values()
    sright = sonar_values["right"] 
    sleft = sonar_values["left"] 
    sfront = sonar_values["front"] 
    sback = sonar_values["back"]  


    if self.is_new_ball_data():
        ball_is_available = 1
        ball_data = self.get_new_ball_data()
        ball_x = ball_data['direction'][0]
        ball_y = ball_data['direction'][1]
        direction = get_direction(ball_data["direction"])
        strength = ball_data["strength"]
    else:
        ball_is_available = 0
        ball_data = None
        direction = None
    ball_angle = math.atan2(ball_y,ball_x)
    ball_angle = math.degrees(ball_angle)
    
    deg_ball_by_robot = (ball_angle + robot_angle)%360

    DistZGoal = math.sqrt((robotx-0)**2 + (roboty-0.7)**2)
    # print(f'DistZGoal : {DistZGoal}')

def go_to(self, x_maghsad, y_maghsad):
    global zavie_maghsad
    global error_zavie
    global error_fasele
    global error
    global delta_x
    global delta_y
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
    if error_fasele > 2 :
        move(self,error_fasele - error+10, error_fasele + error+10)                   
    # else :
    #     if robot_angle > 2:
    #         move(self, 5, -5)   
    #     elif robot_angle < -2:
    #         move(self, -5, 5)  
    #     else:
    #         move(self, 0, 0)
def toop_be_zamin_update(self):
    global toop_be_zamin_x
    global toop_be_zamin_y
    global ball_dist
    global ball_angle
    global ball_angle_predict
    global distance
    global ball_speed
    global now
    global delta_time
    global last_time
    global ball_angle_predict_deg
    global newDeg
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

def mostaghim(self):
    global state 
    global is_turning

    if toop_be_zamin_y > roboty :
        is_turning = 1
    elif deg_ball_by_robot > 350 or deg_ball_by_robot < 10:
        is_turning = 0
               
    if toop_be_zamin_y < roboty:
        if state == 1:
            go_to(self,toop_be_zamin_x,toop_be_zamin_y+0.045)
            if abs(toop_be_zamin_x-robotx) < 0.01 and abs(toop_be_zamin_y-roboty) < 0.01 :
                state = 2
        elif state == 2: 
            go_to(self,toop_be_zamin_x,toop_be_zamin_y) 
            if abs(toop_be_zamin_x-robotx) > 0.2 and abs(toop_be_zamin_y-roboty) > 0.2 :
                state = 1
    else :
        if toop_be_zamin_x > 0 :
            go_to(self,toop_be_zamin_x-0.06,toop_be_zamin_y+0.045)
        elif toop_be_zamin_y < 0:
            go_to(self,toop_be_zamin_x+0.06,toop_be_zamin_y+0.045)

def turn2(self):
    global is_turning

    if toop_be_zamin_y > roboty :
        is_turning = 1
    elif deg_ball_by_robot > 350 or deg_ball_by_robot < 10:
        is_turning = 0

    if is_turning == 0 and toop_be_zamin_y < 0.5:
        if 330>deg_ball_by_robot>30:
            goToTheta(self,deg_ball_by_robot-90)
        else:
            if strength > 250 :
                go_to(self,0,-0.6)
            else :
                goToTheta(self,deg_ball_by_robot-90)

    elif is_turning == 1 and toop_be_zamin_y < 0.5:
        if toop_be_zamin_x < robotx :
            goToTheta(self,deg_ball_by_robot - 90 - (strength / 1.5))
        else :
            goToTheta(self,deg_ball_by_robot - 90 + (strength / 1.5))
    elif roboty > 0.5 :
        go_to(self,0,0.2)


def goal_keeper(self):
    if toop_be_zamin_y < roboty :
        if 0<robotx<0.33 or -0.33<robotx<0:
            go_to(self,toop_be_zamin_x,0.6)
        elif robotx>=0.33:
            go_to(self,0.33,0.6)
        elif robotx<=-0.33:
            go_to(self,-0.33,0.6)
    elif toop_be_zamin_y>roboty and robotx > 0 :
        go_to(self,0.33,toop_be_zamin_y)
    elif toop_be_zamin_y>roboty and robotx < 0 :
        go_to(self,-0.33,toop_be_zamin_y)


def goToTheta(self,MoveTheta):
    go_to(self,robotx+math.cos(MoveTheta*0.0174532925199433)*0.05 , roboty+math.sin(MoveTheta*0.0174532925199433)*0.05)
