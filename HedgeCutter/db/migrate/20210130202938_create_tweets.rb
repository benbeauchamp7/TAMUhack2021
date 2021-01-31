class CreateTweets < ActiveRecord::Migration[6.1]
  def change
    create_table :tweets do |t|
      t.string :username
      t.string :datetime
      t.boolean :isrt
      t.boolean :isquote
      t.string :text
      t.string :quoted_text
    end
  end
end
