require 'date'

class TweetsController < ApplicationController
  helper_method :getStonk

  def index
    @tweets = Tweet.all
    @selected = @tweets.first
    @stock = "GME"
    @timediffs = []

    now = Time.new # time..year, .month, 
    i = 0
    @tweets.each do |tweet|
      tweet_time = Time.parse(tweet.datetime)

      # @timediffs[i] = "#{tweet_time} #{now}"

      time_diff = now.to_i - tweet_time.to_i + 7*60*60

      if time_diff < 60
        @timediffs[i] = "#{time_diff}s ago"
      elsif time_diff < 60*60
        @timediffs[i] = "#{time_diff / 60}m ago"
      elsif time_diff < 60*60*24
        @timediffs[i] = "#{time_diff / 60 / 60}h ago"
      else
        @timediffs[i] = "#{time_diff / 60 / 60 / 24}d ago"
      end

      i += 1

    end
  end

  def getStonk(msg)
    # msg.split.each do |word|
    #   if word.length < 6 and word.first == '$'
    #     Ticker.all.each do |tick|
    #       if tick == word[1..-1]
    #         return word
    #       end
    #     end
    #   end
    # end
    "H"
  end

end
