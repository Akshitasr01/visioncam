import logo from "../assets/LOGOCV.png";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#F5F9FF] flex flex-col justify-center items-center px-6">

      <div className="bg-white shadow-xl rounded-3xl p-10 w-full max-w-md border border-blue-100 text-center">

        <img src={logo} className="w-32 h-32 mx-auto mb-6" />

        <h1 className="text-3xl font-bold text-blue-600 tracking-wide">
          VisionCam
        </h1>

        <button
          onClick={() => (window.location.href = "/user-type")}
          className="mt-10 w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-2xl shadow-md text-lg font-semibold transition active:scale-95"
        >
          Start
        </button>

      </div>
    </div>
  );
}
