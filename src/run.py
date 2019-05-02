import json,math
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import cv2,boto3
from bs4 import BeautifulSoup
import moviepy.editor as mpe
from mutagen.mp3 import MP3

source_img = Image.open("./main/download.png").convert("RGBA")
draw = ImageDraw.Draw(source_img)
width,height=source_img.size
size = (width,height)
out = cv2.VideoWriter('final_output.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 24, size) 
polly_client = boto3.Session(
                        aws_access_key_id="YOUR ACCESS KEY",                     
            aws_secret_access_key="YOUR SECRET ACESS KEY",
            region_name='us-west-2').client('polly')
def text_wrap(text, font, max_width):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text) 
    else:
        # split the line by spaces to get words
        words = text.split(' ')  
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''         
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            # when the line gets longer than the max width do not append the word, 
            # add the line to the lines array
            lines.append(line)    
    return lines

    


font = ImageFont.truetype("arialbd.ttf",20)
res = polly_client.synthesize_speech(VoiceId='Raveena',
                        OutputFormat='mp3', 
                        Text = '<speak><break time="1s"/></speak>',TextType='ssml')
x11=res['AudioStream'].read()
count=0
with open('que.json') as jsonfile:
    x=json.load(jsonfile)
    for y in x["sec_details"][0]["sec_questions"]:
        count+=1
number=0
file = open('speech.mp3', 'wb') 
with open('que.json') as jsonfile:
    question=json.load(jsonfile)
    sec_id=question["sec_details"][0]["sec_id"]
    for section in question["sec_details"][0]["sec_questions"]:
        number+=1
        text_o1=[]
        for z in section["que"]["1"]["q_option"]:
            soup=BeautifulSoup(z,"html5lib")
            text_o1.append(soup.getText())
            
        soup=BeautifulSoup(section["que"]["1"]["q_string"],"html5lib")
        text_q_l=soup.getText().split()
        text_q=""
        for s in text_q_l:
            text_q+=s+" "
        text_qnu="Q."+str(number)
        #print(text_qnu)
        text_o=[]
        text_qno="QUESTION "+str(number)+"/"+str(count);
        with open('ans.json') as jsonfile1:
            answer=json.load(jsonfile1)
            ans1=[]
            ans1=answer[sec_id][section["qid"]]["1"][0]
            if(ans1[0]==1):
                ans=str(0)
            elif(ans1[1]==1):
                ans=str(1)
            elif(ans1[2]==1):
                ans=str(2)
            elif(ans1[3]==1):
                ans=str(3)
        source_img = Image.open("./main/download.png").convert("RGBA")
        draw = ImageDraw.Draw(source_img)
        h,w=0,0
        for i in range(4):
            if(font.getsize(text_o1[i])[0]>w):
                w=font.getsize(text_o1[i])[0]
        for i in range(4):
            if(font.getsize(text_o1[i])[1]>h):
                h=font.getsize(text_o1[i])[1]
          
        
        response = polly_client.synthesize_speech(VoiceId='Raveena',
                        OutputFormat='mp3', 
                        Text = '<speak>Question number '+str(number)+'<break time="1s"/></speak>',TextType='ssml')
        
        file.write(response['AudioStream'].read())
        
        response = polly_client.synthesize_speech(VoiceId='Raveena',
                        OutputFormat='mp3', 
                        Text = '<speak>'+text_q+'<break time="1s"/></speak>',TextType='ssml')
        

        question_speech=response['AudioStream'].read()
        file3=open("speechfinal",'wb')
        file3.write(response['AudioStream'].read())
        file3.close()
        file.write(question_speech)
        audio = MP3("speechfinal.mp3")
        
        time=audio.info.length

        for i in range(len(text_o1)):
            response = polly_client.synthesize_speech(VoiceId='Raveena',
                        OutputFormat='mp3', 
                        Text = '<speak>Option '+chr(65+i)+" "+text_o1[i]+'<break time="1s"/></speak>',TextType='ssml')
            file.write(response['AudioStream'].read())
            
        for i in range(6):
            file.write(x11)
        response = polly_client.synthesize_speech(VoiceId='Raveena',
                        OutputFormat='mp3', 
                        Text = '<speak>Times up the Correct answer is option'+chr(int(ans)+65)+" "+text_o1[int(ans)]+'<break time="1s"/></speak>',TextType='ssml')
        file.write(response['AudioStream'].read())    
            

        draw.text((width/2-50,20),text_qno,fill='rgb(255,165,0)',font=font);
        (x,y)=70,50
        draw.text((x-40, y), text_qnu, fill='rgb(255,255,255)', font=font)
        line_height = font.getsize('hg')[1]
        lines = text_wrap(text_q, font, width-90)
        for line in lines:
            draw.text((x+10, y), line, fill='rgb(255,255,255)', font=font)
            y = y + line_height
        source_img.save("file.png", "PNG")
        img = cv2.imread("file.png")
        for i in range(24*math.ceil(time)):
            out.write(img)
        print(text_o1)
        
        ans_1=(x+10, y+line_height)
        ans_2=(int(width/2+x+10), y+line_height)
        ans_3=(x+10, y+h+100)
        ans_4=(int(width/2+x+10), y+h+100)
        for i in range(1,24):
            button_size_1 = (((w+200)/24)*i, h+20)
            button_img_1=Image.open('./main/a.png').convert("RGBA")
            button_img_1.thumbnail(button_size_1)
            button_draw_1 = ImageDraw.Draw(button_img_1)
            button_draw_1.text((50, 10), text_o1[0], font=font)
            source_img.paste(button_img_1, ans_1)
            source_img.save("file.png", "PNG")
            img = cv2.imread("file.png")
            out.write(img)
        for i in range(1,24):
            button_size_1 = (((w+200)/24)*i, h+20)
            button_img_2=Image.open('./main/b.png').convert("RGBA")
            button_img_2.thumbnail(button_size_1)
            button_draw_2 = ImageDraw.Draw(button_img_2)
            button_draw_2.text((50, 10), text_o1[1], font=font)
            source_img.paste(button_img_2, ans_2)
            source_img.save("file.png", "PNG")
            img = cv2.imread("file.png")
            out.write(img)
        for i in range(1,24):
            button_size_1 = (((w+200)/24)*i, h+20)
            button_img_3=Image.open('./main/c.png').convert("RGBA")
            button_img_3.thumbnail(button_size_1)
            button_draw_3 = ImageDraw.Draw(button_img_3)
            button_draw_3.text((50, 10), text_o1[2], font=font)
            source_img.paste(button_img_3, ans_3)
            source_img.save("file.png", "PNG")
            img = cv2.imread("file.png")
            out.write(img)
        for i in range(1,24):
            button_size_1 = (((w+200)/24)*i, h+20)
            button_img_4=Image.open('./main/d.png').convert("RGBA")
            button_img_4.thumbnail(button_size_1)
            button_draw_4 = ImageDraw.Draw(button_img_4)
            button_draw_4.text((50, 10), text_o1[3], font=font)
            source_img.paste(button_img_4, ans_4)
            source_img.save("file.png", "PNG")
            img = cv2.imread("file.png")
            out.write(img)
        for i in range(6):
            timer_img=Image.open("./main/"+str(i)+'s.png').convert("RGBA")
            timer_img.thumbnail((50,50))
            source_img.paste(timer_img, (int(width/2), y+h+200))
            source_img.save("file.png", "PNG")
            img = cv2.imread("file.png")
            for i in range(24):
                out.write(img)
        tick=Image.open('./main/tick.png').convert("RGBA")
        tick.thumbnail((50,50))
        button_size_1 = (w+250, h+25)
        if(ans==str(1)):
            righta=Image.open('./main/righta.png').convert("RGBA")
            righta.thumbnail(button_size_1)
            right = ImageDraw.Draw(righta)
            right.text((50, 10), text_o1[0], font=font)
            source_img.paste(righta, ans_1)
            source_img.paste(tick, (x+190, y+line_height+10))
        if(ans==str(2)):
            rightb=Image.open('./main/rightb.png').convert("RGBA")
            rightb.thumbnail(button_size_1)
            right = ImageDraw.Draw(rightb)
            right.text((50, 10), text_o1[1], font=font)
            source_img.paste(rightb, ans_2)
            source_img.paste(tick, (int(width/2+x+10)+180, y+line_height+10))
        if(ans==str(3)):
            
            rightc=Image.open('./main/rightc.png').convert("RGBA")
            rightc.thumbnail(button_size_1)
            right = ImageDraw.Draw(rightc)
            right.text((50, 10), text_o1[2], font=font)
            source_img.paste(rightc, ans_3)
            source_img.paste(tick, (x+190, y+h+110))
        if(ans==str(4)):
    
            rightd=Image.open('./main/rightd.png').convert("RGBA")
            rightd.thumbnail(button_size_1)
            right = ImageDraw.Draw(rightd)
            right.text((50, 10), text_o1[3], font=font)
            source_img.paste(rightd, ans_4)
            source_img.paste(tick, (int(width/2+x+10)+180, y+h+110))


        timer_end_img=Image.open('./main/timeisup.png').convert("RGBA")
        timer_img.thumbnail((50,50))
        source_img.paste(timer_end_img, (int(width/2-100), y+h+200))

        #source_img.save("./images/12.png", "PNG")
        #source_img.save("./images/13.png", "PNG")
        #source_img.save("./images/14.png", "PNG")
        source_img.save("file.png", "PNG")
        img = cv2.imread("file.png")
        for i in range(24*3):
                out.write(img)
        
out.release()
file.close()

my_clip = mpe.VideoFileClip('final_output.mp4')
audio_background = mpe.AudioFileClip('speech.mp3')
final_audio = mpe.CompositeAudioClip([my_clip.audio, audio_background])
final_clip = my_clip.set_audio(final_audio)

                        
                    
                    

