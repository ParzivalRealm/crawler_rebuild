require "test_helper"

class PartNumbersControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get part_numbers_index_url
    assert_response :success
  end

  test "should get show" do
    get part_numbers_show_url
    assert_response :success
  end

  test "should get new" do
    get part_numbers_new_url
    assert_response :success
  end

  test "should get create" do
    get part_numbers_create_url
    assert_response :success
  end

  test "should get edit" do
    get part_numbers_edit_url
    assert_response :success
  end

  test "should get update" do
    get part_numbers_update_url
    assert_response :success
  end

  test "should get destroy" do
    get part_numbers_destroy_url
    assert_response :success
  end
end
