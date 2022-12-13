import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from db_driver import get_events

from collections import defaultdict

from datetime import datetime, timedelta

from requests import get
from io import BytesIO

from naff import Guild

from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def generate_leaderboard_plot(guild: Guild) -> BytesIO:
    events = get_events()

    # Generate a dictionary of user IDs to timestamps of nuts
    user_dict = defaultdict(list)
    user_avatars = {}

    for event in events:
        user_dict[event[1]].append(event[2])

    # Parse timestamps into a list of dates
    for user in user_dict:
        for idx, entry in enumerate(user_dict[user]):
            utc_date = datetime.strptime(entry, "%Y-%m-%d %H:%M:%S")
            # Convert from UTC to EST

            time_diff = timedelta(hours=5)

            user_dict[user][idx] = utc_date - time_diff

    # Download profile pictures of the users
    for user_id in user_dict.keys():
        user = guild.get_member(user_id)

        avatar_url = user.display_avatar.url

        # Modify url so that the resolution is 128x128
        # The url has a format "...?size=xxxx" so we can just replace the size
        # Drop everything after the ? and add the new size
        avatar_url = avatar_url.split("?")[0] + "?size=128"

        response = get(avatar_url)

        img_file = BytesIO(response.content)

        # convert to matplotlib image
        user_avatars[user_id] = mpimg.imread(img_file)

    plt.style.use('dark_background')

    # Generate the plot
    fig = Figure(figsize=(14, 10))
    ax = fig.add_subplot(111)

    for user_id, timestamps in user_dict.items():

        # Add December 1st 00:00:00 to the list of timestamps
        timestamps = [datetime(2022, 12, 1, 0, 0, 0)] + timestamps

        # Generate cumulative sum of nuts
        cum_nuts = []
        for i in range(len(timestamps)):
            cum_nuts.append(i)

        # Plot using post-steps
        ax.step(timestamps, cum_nuts, 'o-', where="post")

        # Add profile picture to the plot on the last nut
        imagebox = OffsetImage(user_avatars[user_id], zoom=0.2)
        annotation = AnnotationBbox(imagebox, (timestamps[-1], cum_nuts[-1]), pad=0, frameon=False)
        ax.add_artist(annotation)
        
    ax.set_title("Nuts over time, December 2022")

    # label axes
    ax.xaxis.set_label_text("Date")
    ax.yaxis.set_label_text("Number of Nuts")
    
    fig.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    return buffer
    
if __name__ == "__main__":
    generate_leaderboard_plot()