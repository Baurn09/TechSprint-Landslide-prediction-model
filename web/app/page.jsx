
import Link from "next/link";

import { Inter, Share_Tech, Space_Grotesk } from "next/font/google";
import Image from "next/image";
const bungee = Share_Tech({
  subsets: ["latin"],
  weight: "400",
});
const InfoBlock = ({ title, description, image, children, reverse }) => {
    return (
      <div
        className={`max-w-7xl mx-auto px-4 flex flex-col ${
          reverse ? "lg:flex-row-reverse" : "lg:flex-row"
        } items-center gap-8`}
      >
        {/* Text Card */}
        <div className="w-full lg:w-1/2 bg-[#DAF1DE] border-2 border-[#839a87] rounded-xl shadow-md p-6">
          <h2 className="bg-[#163832] text-white text-2xl font-bold rounded-lg p-4 mb-6">
            {title}
          </h2>

          {description && (
            <p className="text-gray-600 leading-relaxed">{description}</p>
          )}

          {children && <div className="mt-6 space-y-4">{children}</div>}
        </div>

        {/* Image Container */}
        <div className="w-full lg:w-1/2 h-full flex items-stretch">
          <div className="w-full h-full rounded-xl border-2 border-[#839a87] overflow-hidden">
            <img
              src={image}
              alt=""
              className="w-full h-full object-contain"
            />
          </div>
        </div>

      </div>
    );
  };

  const Step = ({ title, text }) => {
    return (
      <div>
        <h3 className="font-semibold text-black">• {title}</h3>
        <p className="text-gray-600 mt-1 pl-4">{text}</p>
      </div>
    );
  };


export default function Home() {
  return (
    <main className={`bg-[#F2EFEA] ${bungee.className} `}>
      <section className="relative w-full bg-[url('/mim2.png')] h-screen overflow-hidden">
          <div className="relative z-10 flex flex-col items-center justify-center h-full text-center text-white">
            <header className="px-8 py-4 absolute top-5 left-[20%] w-[60vw]">
              <div className="navbar flex justify-between shadow-sm rounded-xl  bg-[#163832] ">
                <div>
                  <a className="btn btn-ghost text-xl text-white">M.I.M</a>
                </div>
                <div className="flex gap-12 items-center justify-center">
                  <Link href="/" className=" text-white hover:text-blue-600">Home</Link>
                  <Link href="/components/map" className="text-white hover:text-black">Map</Link>
                  <Link href="/admin" className="text-white hover:text-black">Admin</Link>
                  <div className="dropdown dropdown-end">
                    <div tabIndex={0} role="button" className="btn btn-ghost btn-circle avatar">
                      
                      <div className="w-10 rounded-full">
                        <Image
                          width={10}
                          height={10}
                          alt="Tailwind CSS Navbar component"
                          src="/land1.jpeg" />
                      </div>
                    </div>
                    <ul
                      tabIndex="-1"
                      className="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow">
                      <li>
                        <a className="justify-between">
                          Profile
                          <span className="badge">New</span>
                        </a>
                      </li>
                      <li><a>Settings</a></li>
                      <li><a>Logout</a></li>
                    </ul>
                  </div>
                </div>
              </div>
            </header>
          
            <h1 className="transition-all hover:scale-105 text-8xl text-white font-bold mb-4">
              AI-Based Environmental &
            </h1>
            <h1 className="transition-all hover:scale-105 text-8xl text-white font-bold mb-4">
              Disaster Risk Forecasting
            </h1>
            <p className="text-lg text-stone-300">
              Real-time landslide risk prediction using satellite data,
              ground sensors, and machine learning.
            </p>
            
            <a
                href="/components/map"
                className="mx-4 hover:bg-[#051f20] hover:-translate-y-1 shadow-md hover:shadow-lg hover:scale-105 transition-all inline-block mt-8 px-6 py-3 bg-[#163832] text-white rounded-4xl"
              >
                View Map →
            </a>
          </div>
      </section>
      <section className="bg-[#163832] py-12 w-full flex flex-col gap-16">
        {/* Section 1 */}
        <InfoBlock
          title="Landslide History in Manipur"
          description="Manipur experiences frequent landslides, particularly during the monsoon season. Over the past years, repeated slope failures have caused loss of lives, damaged roads, and disrupted connectivity in hilly districts."
          image="/his.png"   // 📊 map / chart / photo
          reverse={false}
        >
          <ul className="text-gray-600 list-disc list-inside space-y-2">
            <li>🌧️ High landslide occurrence during intense monsoon months</li>
            <li>🚧 Frequent road blockages disrupting transport and supply chains</li>
            <li>🏘️ Village isolation due to damaged roads and communication links</li>
            <li>📉 Limited early-warning coverage in remote and hilly regions</li>
            <li>🚑 Delayed emergency response caused by poor accessibility</li>
            <li>🗺️ Lack of localized, grid-level risk monitoring</li>
            <li>📝 Dependence on manual reporting and post-event assessment</li>
          </ul>


        </InfoBlock>


        {/* Section 2 */}
        <InfoBlock
          title="Soil & Terrain Characteristics of Manipur"
          description="Manipur’s hilly regions consist of weathered soil, steep slopes, and varying vegetation cover, making them highly susceptible to rainfall-triggered landslides."
          image="/soilmap.jpeg"   // 🗺️ soil / terrain map
          reverse={true}
        >
          <ul className="text-gray-600 list-disc list-inside space-y-2">
            <li>🧱 Mixed soil composition with low shear strength</li>
            <li>⛰️ Steep slopes with fragile and highly weathered hill formations</li>
            <li>🌧️ High rainfall infiltration during monsoon seasons</li>
            <li>💧 Poor natural drainage leading to water accumulation</li>
            <li>🌱 Loss of vegetation cover increasing surface erosion</li>
            <li>🪨 Frequent soil saturation reducing slope stability</li>
            <li>⚠️ Natural and human-induced slope disturbances</li>
          </ul>
        </InfoBlock>


        {/* Section 3 */}
        <InfoBlock
          title="How Our Landslide Monitoring System Works"
          image="/RegenWorkflow.jpeg"   // 🔄 workflow / diagram
          reverse={false}
        >
          <Step
            title="🗺️ Grid-Based Area Division"
            text="The entire region is divided into uniform grid cells to enable localized and independent monitoring."
          />

          <Step
            title="🛰️ Satellite-Based Risk Identification"
            text="Satellite and geospatial data are analyzed per grid to classify baseline landslide susceptibility."
          />

          <Step
            title="🧱 Proxy-Based Soil Strength Characterization"
            text="Soil strength is inferred using soil maps, surveys, and related proxies instead of direct testing."
          />

          <Step
            title="📜 Historical Landslide Data Integration"
            text="Past landslide records are incorporated to enhance grid-level risk understanding."
          />

          <Step
            title="📍 Ground Sensor Deployment"
            text="Custom multi-sensor nodes are deployed selectively in high-risk grids."
          />

          <Step
            title="⏱️ Real-Time Data Collection"
            text="Sensors continuously collect soil moisture, tilt, vibration, and acceleration data."
          />

          <Step
            title="📡 Data Transmission"
            text="Sensor data is transmitted with grid ID and timestamps using LoRa or low-bandwidth networks."
          />

          <Step
            title="🤖 ML-Based Risk Calculation"
            text="Machine learning models combine static and dynamic features to estimate landslide probability per grid."
          />

          <Step
            title="🚨 Multi-Level Alert Generation"
            text="Risk probabilities are converted into watch, warning, or emergency alert levels."
          />

          <Step
            title="👮 Authority-Focused Alert Dissemination"
            text="Grid-specific alerts are delivered to relevant authorities via dashboards, SMS, or APIs."
          />

          <Step
            title="🔁 Continuous Learning & Improvement"
            text="New sensor data and events are used to periodically retrain and improve the model."
          />


        </InfoBlock>

        <InfoBlock
          title="What Makes Our System Unique"
          image="/RegenFlow.png"   // ⭐ abstract / sensor / map
          reverse={true}
        >
          <ul className="text-gray-600 list-disc list-inside space-y-2">
            <li>🚨 Authority-focused, grid-specific landslide alerts</li>
            <li>🛰️ Integrated satellite and ground sensor data fusion</li>
            <li>🗺️ Fixed grid-based, highly localized monitoring architecture</li>
            <li>🧱 Proxy-based soil strength estimation per grid</li>
            <li>🌱 Custom multi-sensor nodes for hilly and remote terrain</li>
            <li>⏱️ Near real-time, continuous data acquisition</li>
            <li>🤖 ML-based landslide probability estimation</li>
            <li>📡 Low-connectivity LoRa-based communication</li>
          </ul>
        </InfoBlock>
      </section>
    </main>
  );
}
