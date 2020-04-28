# frozen_string_literal: true

class UserSerializer < ActiveModel::Serializer
  attributes :first_name, :last_name, :email
end
