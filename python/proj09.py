'''Skeleton file with all strings for Mimir testing'''

import string, calendar
from operator import itemgetter
import pylab

MONTH_NAMES = [calendar.month_name[month] for month in range(1,13)]

def open_file():
    while True:
        filename = input("Input a filename: ")
        try:
            file_handle = open(filename, 'r')
            return file_handle
        except Exception:
            print("Error in input filename. Please try again.")

def validate_hashtag(s):
    '''The function validate_hashtag has a string which is
       a hastag.
    '''
    s = s[1:]
    if s.isdigit():
        return False
    for punc in string.punctuation:
        if punc in s:
            return False
    return True

def get_hashtags(s):
    '''The function get_hashtags has a string which is a tweet.'''
    tweet = []
    beginning = s.find('#')
    while(beginning	!= -1):
        end	= s.find(' ', beginning)
        tag = ""
        if end == -1:
            tag = s[beginning:]
        else:
            tag = s[beginning:end]
        tweet.append(tag)
        beginning = s.find('#',end)

    valid_hashtags = []
    for hashtag in tweet:
        if hashtag.find("#") == 0 and validate_hashtag(hashtag):
            valid_hashtags.append(hashtag)
    return valid_hashtags

def read_data(fp):
    '''The function read_data reads in the data collecting 3 things 
       from each row:  username as string, month as integer, and a
       list of all hashtags found in the tweet message.
    '''
    result = []
    for line in fp:
        row = line.strip().split(",")
        valid_hashtags = get_hashtags(row[2])
        result.append([row[0], int(row[1]), valid_hashtags])

    return result


def get_histogram_tag_count_for_users(data,usernames):
    '''The function get_histogram_tag_count_for_users creates a histogram
       of hashtags for how often they occur.
    '''
    histogram = {}
    for user_data in data:
        if user_data[0] in usernames:
            for hashtag in user_data[2]:
                if hashtag in histogram:
                    histogram[hashtag] += 1
                else:
                    histogram[hashtag] = 1

    return histogram

def get_tags_by_month_for_users(data,usernames):
    '''The function get_tags_by_month_for_users builds a set of unique hashtags
       grouped by the month in which they are used.
    '''
    tags = []
    for i in range(1, 13):
        tags.append((i, set()))
    for index, tag in enumerate(tags):
        for user_data in data:
            if user_data[0] in usernames and int(user_data[1]) == tag[0]:
                for hashtag in user_data[2]:
                    tags[index][1].add(hashtag)

    tags = sorted(tags, key=itemgetter(0))

    return tags

def get_user_names(L):
    '''The function get_user_names returns a sorted list of user names that are
       in the twitter data.
    '''
    usernames = list(set([data[0] for data in L]))
    usernames.sort()

    return usernames

def three_most_common_hashtags_combined(L,usernames):
    '''The function three_most_common_hashtags_combined returns an ordered list
       of three tuples where count is the count of all occurances of hashtag
       across all users in usernames.
    '''
    histogram = get_histogram_tag_count_for_users(L, usernames)
    sorted_histogram = sorted(histogram.items(), key=itemgetter(1), reverse=True)
    sorted_histogram = [(v, k) for k, v in sorted_histogram[:3]]

    return sorted_histogram

def three_most_common_hashtags_individuals(data_lst,usernames):
    '''The function three_most_common_hashtags_individuals returns an ordered
       list of three tuples where count is the count of occurences of hashtag
       only for a user in usernames.
    '''
    result = []
    for username in usernames:
        histogram = get_histogram_tag_count_for_users(data_lst, [username])
        for hashtag, count in histogram.items():
            result.append((count, hashtag, username))
    result = sorted(result, key=itemgetter(0), reverse=True)

    return result[:3]

            
def similarity(data_lst,user1,user2):
    '''The function similarity compares the hashtags used by each user for each
       month and returns the numbers of hashtags which were used by both
       accounts in that month.
    '''
    similarity_lst = []

    user1_tag_data = get_tags_by_month_for_users(data_lst, [user1])
    user2_tag_data = get_tags_by_month_for_users(data_lst, [user2])

    for index, user1_tag in enumerate(user1_tag_data):
        intersection = user2_tag_data[index][1].intersection(user1_tag[1])
        similarity_lst.append((user1_tag[0], intersection))
    
    return similarity_lst

        
def plot_similarity(x_list,y_list,name1,name2):
    '''Plot y vs. x with name1 and name2 in the title.'''
    
    pylab.plot(x_list,y_list)
    pylab.xticks(x_list,MONTH_NAMES,rotation=45,ha='right')
    pylab.ylabel('Hashtag Similarity')
    pylab.title('Twitter Similarity Between '+name1+' and '+name2)
    pylab.tight_layout()
    pylab.show()
    #the next line is simply to illustrate how to save the plot
    #leave it commented out in the version you submit
    #pylab.savefig("plot.png")


def main():
    
    # Open the file
    fp = open_file()
    # Read the data from the file
    d = read_data(fp)
    # Create username list from data
    usernames_str = get_user_names(d)
    # Calculate the top three hashtags combined for all users
    three_most_combined = three_most_common_hashtags_combined(d, usernames_str)
    # Print them
    # Calculate the top three hashtags individually for all users
    three_most_indv = three_most_common_hashtags_individuals(d, usernames_str)
    # Print them
    # Prompt for two user names from username list
    # Calculate similarity for the two users
    # Print them
    # Prompt to plot or not and plot if 'yes'
    print("")
    print("Top Three Hashtags Combined")
    print("{:>6s} {:<20s}".format("Count","Hashtag"))

    # your printing loop goes here
    for count, hashtag in three_most_combined:
        print("{:>6s} {:<20s}".format(str(count),hashtag))
    print("")
    
    print("Top Three Hashtags by Individual")
    print("{:>6s} {:<20s} {:<20s}".format("Count","Hashtag","User"))
    for count, hashtag, user in three_most_indv:
        print("{:>6s} {:<20s} {:<20s}".format(str(count),hashtag,user))
    print("")

    print("Usernames: ", ", ".join(usernames_str))

    user_str = ""
    while True:  # prompt for and validate user names
        user_str = input("Input two user names from the list, comma separated: ")
        user_str = user_str.split(",")
        if len(user_str) < 2 or user_str[0].strip() not in usernames_str or user_str[1].strip() not in usernames_str:
            str_12="Error in user names.  Please try again"
            print(str_12.strip())
            print
            continue
        break
    user1 = user_str[0].strip()
    user2 = user_str[1].strip()
    # calculate similarity here
    similar = similarity(d, user1, user2)
    print()
    print("Similarities for " + user1 + " and " + user2)
    print("{:12s}{:6s}".format("Month","Count"))

    # your printing loop goes here
    for month, count in similar:
        print("{:12s}{:6s}".format(MONTH_NAMES[month - 1],str(len(count))))
    print()
    # Prompt for a plot
    choice = input("Do you want to plot (yes/no)?: ")
    if choice.lower() == 'yes':
        # create x_list and y_list
        x_list = list(range(1, 13))
        y_list = [ count(month) for month, count in similar]
        plot_similarity(x_list, y_list, user_str[0], user_str[1])

if __name__ == '__main__':
    main()