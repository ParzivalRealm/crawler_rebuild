# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2023_01_30_172335) do
  create_table "attachments", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "file"
    t.string "attachable_type"
    t.integer "attachable_id"
    t.index ["attachable_type", "attachable_id"], name: "index_attachments_on_attachable_type_and_attachable_id"
  end

  create_table "attachments_scrappers", id: false, force: :cascade do |t|
    t.integer "scrapper_id", null: false
    t.integer "attachment_id", null: false
    t.index ["attachment_id", "scrapper_id"], name: "index_attachments_scrappers_on_attachment_id_and_scrapper_id"
    t.index ["scrapper_id", "attachment_id"], name: "index_attachments_scrappers_on_scrapper_id_and_attachment_id"
  end

  create_table "part_numbers", force: :cascade do |t|
    t.string "part_number", null: false
    t.string "description", null: false
    t.string "manufacturer", null: false
    t.string "category"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "part_numbers_scraped_data", id: false, force: :cascade do |t|
    t.integer "part_number_id", null: false
    t.integer "scraped_datum_id", null: false
    t.index "\"part_number\"", name: "index_part_numbers_scraped_data_on_part_number"
    t.index "\"scraped_data\"", name: "index_part_numbers_scraped_data_on_scraped_data"
  end

  create_table "part_numbers_suppliers", id: false, force: :cascade do |t|
    t.integer "part_number_id", null: false
    t.integer "supplier_id", null: false
    t.index ["part_number_id"], name: "index_part_numbers_suppliers_on_part_number_id"
    t.index ["supplier_id"], name: "index_part_numbers_suppliers_on_supplier_id"
  end

  create_table "scraped_data", force: :cascade do |t|
    t.integer "supplier_id"
    t.integer "scrapper_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "data_type"
    t.string "data_value"
    t.string "part_number"
  end

  create_table "scrappers", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "price"
    t.integer "availablequantity"
    t.integer "minimumorderquantity"
    t.integer "leadtime"
  end

  create_table "suppliers", force: :cascade do |t|
    t.string "name"
    t.string "website"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "searchpath"
  end

  create_table "users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "attachment_id"
    t.string "attachable"
    t.integer "role", default: 0
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
    t.index ["role"], name: "index_users_on_role"
  end

end
