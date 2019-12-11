import matplotlib.pyplot as plt
from PIL import Image


def figure_save(pg1, pg2, save_to, suptitle='', pg1_title='', pg2_title=''):
    fig = plt.figure()
    fig.suptitle(suptitle)

    if not isinstance(pg1, Image.Image):
        pg1 = Image.open(pg1)

    if not isinstance(pg2, Image.Image):
        pg2 = Image.open(pg2)

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.title.set_text(pg1_title)
    plt.imshow(pg1)

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.title.set_text(pg2_title)
    plt.imshow(pg2)

    # plt.show()
    plt.savefig(save_to)
    plt.close(fig)
