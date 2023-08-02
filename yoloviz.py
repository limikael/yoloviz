#!/usr/bin/env python3

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import click

def make_result_comps(result, n, wh):
    w,h=result.masks.data.shape[1],result.masks.data.shape[2]

    data=bytes()
    for y in range(h):
        for x in range(w):
            if result.masks.data[n][y][x]>.5:
                data+=b'\x00\xff\xff\x80'

            else:
                data+=b'\x00\x00\x00\x00'

    mask_im=pygame.image.frombytes(data,(w,h),"RGBA")
    mask_im_scaled=pygame.transform.scale(mask_im,wh)

    points=[]
    xy=result.masks.xy[n]
    for i in range(xy.shape[0]):
        points.append((float(xy[i][0]),float(xy[i][1])))

    xywh=result.boxes.xywh[n]
    #print("xywh: ",xywh)
    rect=(float(xywh[0]-xywh[2]/2),float(xywh[1]-xywh[3]/2),float(xywh[2]),float(xywh[3]))

    font = pygame.font.Font('freesansbold.ttf', 12)
    pct=round(float(result.boxes.conf[n]*100))
    text = font.render(result.names[0]+": "+str(pct)+"%", True, (0,0,0), (128,255,255))

    return {
        "points": points,
        "rect": rect,
        "text": text,
        "mask": mask_im_scaled
    }

def show(results):
    result=results[0]

    pygame.init()
    pygame.display.set_caption('YOLO')

    im=pygame.image.load(result.path)
    wh=(im.get_width(),im.get_height())
    display=pygame.display.set_mode(wh)

    comps=[]
    for i in range(result.boxes.shape[0]):
        comps.append(make_result_comps(result,i,wh))

    quit=False
    while not quit:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    quit=True

                case pygame.VIDEOEXPOSE:
                    display.blit(im,(0,0))

                    for r in comps:
                        display.blit(r["mask"],(0,0))
                        pygame.draw.polygon(display,(128,255,255),r["points"],2)
                        pygame.draw.rect(display,(128,255,255),r["rect"],2)
                        display.blit(r["text"],(r["rect"][0],r["rect"][1]))

                    pygame.display.update()

    pygame.display.quit()

@click.command()
@click.option('--model', help='The YOLO model.pt file.', required=True)
@click.option('--conf', help='Confidence threshold in percent.', type=float, default=50)
@click.argument('filename')
def yoloshow_cli(filename, model, conf):
    from ultralytics import YOLO
    model=YOLO(model)
    results=model(filename,conf=conf/100.0)
    show(results)

if __name__=="__main__":
    yoloshow_cli()
