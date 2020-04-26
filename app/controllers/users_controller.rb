class UsersController < ApplicationController
  skip_before_action :verify_authenticity_token

    def index
      render json: User.all, each_serializer: UserSerializer
    end

    def show
      render json: User.find(params[:id])
    end

    def create
      @user = User.create(user_params)
      render json: @user.to_json
    end

    def user_params
      params.require(:user).permit(:first_name, :last_name, :email)
    end
  end