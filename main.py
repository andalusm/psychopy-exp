from trial import *
question = "Which is the odd one out?"
img_source = 'im.mat'


if __name__ == "__main__":
    try:
        os.mkdir("imgs")
        os.mkdir("logs")
    except:
        pass
    db = Database(img_source,trial_num=100, load_imgs = False)
    all_imgs = db.get_all_trial_imgs()
    vs = Visuals(question,all_imgs,3)
    vs.runner()


