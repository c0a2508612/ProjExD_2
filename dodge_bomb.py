from tkinter import W
from asyncio import ReadTransport
import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """入力されたRectの座標をチェックして、画面外であればTrue、画面内ではFalseを返す。

    Args:
        rct (pg.Rect): 対象のRect

    Returns:
        tuple[bool, bool]: 0番要素はX軸が画面外であればTrue, 画面内はFalse 1番要素はY軸が画面外であればTrue, 画面内はFalse
    """
    yoko, tate = False, False
    if rct.left < 0 or rct.right > WIDTH:
        yoko = True
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = True
    
    return yoko, tate

def move_bound(rct: pg.Rect):
    """入力されたRectの座標をチェックして、画面外であれば移動をブロックする。(独自実装)

    Args:
        rct (pg.Rect): 対象のRect
    """
    if rct.top < 0:
        rct.top = 0
    if rct.bottom > HEIGHT:
        rct.bottom = HEIGHT
    if rct.left < 0:
        rct.left = 0
    if rct.right > WIDTH:
        rct.right = WIDTH

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # 爆弾のためのSurface
    bb_img = pg.Surface((20, 20))
    # 円を描く
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), (10))
    # bb_imgの背景色を抜く(カラーキー)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    # 初期座標はランダム
    bb_rct.move_ip(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    # 爆弾の移動速度を定義
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, 5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (5, 0)
    }
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        # この方法だとX,Y軸どちらかが衝突した場合に、衝突していない片方の軸の移動ができなくなる
        if check_bound(kk_rct) != (False, False):
             kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        # move_bound(kk_rct)
        screen.blit(kk_img, kk_rct)
        # 爆弾をうごかす
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if yoko:
            vx *= -1
        if tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
