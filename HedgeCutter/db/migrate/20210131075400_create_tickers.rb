class CreateTickers < ActiveRecord::Migration[6.1]
  def change
    create_table :tickers do |t|
      t.string :symbol

      t.timestamps
    end
  end
end
