import mongoose,{ model, Document, Schema } from "mongoose";
import dotenv from "dotenv";


dotenv.config();


export const connectDB = async () => {
  if (!process.env.DATABASE_URL) {
    throw new Error("DATABASE_URL is not defined");
  }


  try {
    await mongoose.connect(process.env.DATABASE_URL);
    console.log("MongoDB connected");
  } catch (err) {
    console.error("MongoDB connection error:", err);
    process.exit(1);
  }
};


const UserSchema = new Schema(
  {
    username: {
      type: String,
      required: true,
      unique: true,
      minlength: 2,
      maxlength: 100,
      trim: true,
    },

    age: {
      type: Number,
      required: true,
      min: 1,
      max: 120,
    },

    gender: {
      type: String,
      required: true,
      enum: ["male", "female", "other"],
    },

    phone: {
      type: String,
      required: true,
      match: /^[6-9]\d{9}$/,
    },

    emergencyname: {
      type: String,
      required: true,
      trim: true,
    },

    emergencyphone: {
      type: String,
      required: true,
      match: /^[6-9]\d{9}$/,
    },

    password: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true, // createdAt & updatedAt
  }
);
export const UserModel= model("User" , UserSchema)


export interface UserType extends Document {
  username: string;
  password: string;


}// interface for existing user
