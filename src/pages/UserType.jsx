export default function UserType() {
  return (
    <div className="min-h-screen bg-[#F5F9FF] flex justify-center items-center px-6">

      <div className="bg-white p-8 rounded-3xl shadow-xl border border-blue-100 w-full max-w-md">

        <h2 className="text-2xl font-bold text-center text-blue-600 mb-8">
          Continue as
        </h2>

        <button
          onClick={() => (window.location.href = "/login")}
          className="w-full bg-blue-600 text-white py-3 rounded-xl mb-4 text-lg shadow hover:bg-blue-700 active:scale-95"
        >
          Existing User
        </button>

        <button
          onClick={() => (window.location.href = "/signup")}
          className="w-full border border-blue-600 text-blue-600 py-3 rounded-xl text-lg shadow hover:bg-blue-50 active:scale-95"
        >
          New User
        </button>

      </div>
    </div>
  );
}
