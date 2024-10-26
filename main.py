from trial import *
question = "Which is the odd one out?"
img_source = 'im.mat'


if __name__ == "__main__":
    db = Database(img_source,trial_num=3, load_imgs = False)
    all_imgs = db.get_all_trial_imgs()
    vs = Visuals(question,all_imgs,3)
    vs.runner()


