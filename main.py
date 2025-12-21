import cv2
from ultralytics import YOLO
import time
import threading
import vlc

playback_lock=threading.Lock()
is_playing= False
current_player= None

def watch_play(player):
	global is_playing,current_player
	try:
		time.sleep(0.1)
		while True:
			try:
				playing=player.is_playing()
			except Exception:
				playing = False
			if not playing:
				time.sleep(0.1)
				if not player.is_playing():
				 	break
			time.sleep(0.1)
	finally:
		with playback_lock:
			try:
				player.stop()
			except Exception:
				pass
			if current_player is player:
				current_player=None
				is_playing=False

def play_video(path,reset=False):
	global is_playing,current_player
	if 'vlc' not in globals() or vlc is None:
		print("python-vlc not available — skipping playback.")
		return
	with playback_lock:
		if is_playing:
			if not reset:
				return
			try:
				if current_player :
					current_player.stop()
			except Exception:
				pass
			is_playing=False
			current_player=None
		try:
			player=vlc.MediaPlayer(path)
		except Exception as e:
			print(f"Error creating player: {e}")
			return
	    
		current_player=player
		is_playing=True
		player.play()
		threading.Thread(target=watch_play,args=(player,),daemon=True).start()


buffer=[0,0,0,0,0]
buffer_size= len(buffer)
cool_time=30
trigger=3
last_tri_time=0.0
cam=cv2.VideoCapture(0)
model=YOLO("yolov8s.pt")
ret,frame=cam.read()
frame_count=0

while True:
	ret,frame=cam.read()
	if not ret or frame is None:
		time.sleep(0.05)
		continue
	result=model(frame)
	result=result[0]
	found=False
	if len(result.boxes.cls):
		cls_list=[int(x) for x in result.boxes.cls.tolist()]
		conf_list=[float(x) for x in result.boxes.conf.tolist()]
		boxes=[list(map(float,b)) for b in result.boxes.xyxy.tolist()]
		h,w=frame.shape[:2]
		frame_area=w*h
		for cls,conf,box in zip(cls_list,conf_list,boxes):
			if cls==67 and conf>=0.4:
				x1,y1,x2,y2=box
				area=max(0.0,(x2-x1)*(y2-y1))
				if area>=0.02*frame_area:
					found=True
					break
	buffer.pop(0)
	buffer.append(1 if found else 0)
	t=time.time()
	hits=sum(buffer)
	cooldown_remaining=max(0,cool_time-(t-last_tri_time))
	if hits>3 and cooldown_remaining<=0:
		 print("[trigger] conditions met -> attempting to play video")
		 play_video("E:\LPU\PROJECTS\study_gaurd\VID_20251124_121454_078.mp4",reset=False)
		 last_tri_time=t
		 buffer=[0]*buffer_size


	cv2.putText(frame, f"Buffer:{buffer} Hits:{hits}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
	cv2.putText(frame, f"Cooldown:{cooldown_remaining:.1f}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
	cv2.imshow("Study_Guard", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()
with playback_lock:
    try:
        if current_player:
            current_player.stop()
    except Exception:
        pass
