import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

ListofPup = pd.read_csv('spideroutput')
titles = ListofPup.title # get the titles section to be passed to the word cloud
# convert it to strings
titlesString = [''.join(str(title)) for title in titles] 
titlesString = str(titlesString)
# create the wordcloud
word_cloud = WordCloud(collocations = False, background_color = 'white').generate(titlesString)
# plot and save the wordcloud 
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show()
plt.savefig("MohamedResearch.png",dpi = 300)