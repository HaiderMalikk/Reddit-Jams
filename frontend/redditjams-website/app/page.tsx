import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-white font-sans overflow-x-hidden">
      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 md:px-8 py-12">
        {/* Welcome Section with Input */}
        <section className="mb-20 text-center">
          <h2 className="mb-8 text-4xl font-bold text-black">
            Welcome to Reddit<span className="text-primary">Jams</span>
          </h2>
          <div className="mx-auto flex flex-col md:flex-row max-w-2xl gap-4">
            <input
              type="text"
              placeholder="Paste Spotify playlist link..."
              className="flex-1 rounded-lg border-2 border-black px-6 py-4 text-black placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <button className="rounded-lg bg-primary px-8 py-4 font-semibold text-white transition-colors hover:bg-[#E63D00] md:whitespace-nowrap">
              Start
            </button>
          </div>
        </section>

        {/* Info Section */}
        <section className="mb-20">
          <div className="rounded-lg border-2 border-black bg-white p-8 shadow-lg">
            <h3 className="mb-4 text-center text-2xl font-bold text-primary">
              Discover Your Next Favorite Song
            </h3>
            <p className="mb-6 text-center text-lg text-black">
              RedditJams analyzes your Spotify playlist, searches Reddit's music
              community, and uses AI to generate personalized song recommendations
              just for you.
            </p>
            <div className="grid gap-6 md:grid-cols-3">
              <div className="text-center">
                <div className="mb-2 text-4xl font-bold text-primary">1</div>
                <h4 className="mb-2 font-semibold text-black">
                  Analyze Your Playlist
                </h4>
                <p className="text-sm text-gray-700">
                  We extract your top tracks and artists based on popularity to
                  understand your music taste
                </p>
              </div>
              <div className="text-center">
                <div className="mb-2 text-4xl font-bold text-primary">2</div>
                <h4 className="mb-2 font-semibold text-black">Search Reddit</h4>
                <p className="text-sm text-gray-700">
                  We find music recommendation posts from r/music community that
                  match your preferences
                </p>
              </div>
              <div className="text-center">
                <div className="mb-2 text-4xl font-bold text-primary">3</div>
                <h4 className="mb-2 font-semibold text-black">
                  AI-Powered Results
                </h4>
                <p className="text-sm text-gray-700">
                  AI everything and delivers 5 personalized song
                  recommendations with Spotify links
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* How to Use Section */}
        <section className="mb-20">
          <h3 className="mb-8 text-center text-3xl font-bold text-black">
            How to Get Your Spotify Playlist Link
          </h3>
          <div className="space-y-8">
            {/* Step 1 */}
            <div className="flex gap-6 rounded-lg border-2 border-black p-6">
              <div className="flex-shrink-0">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary text-xl font-bold text-white">
                  1
                </div>
              </div>
              <div className="flex-1">
                <h4 className="mb-2 text-xl font-semibold text-black">
                  Open Spotify
                </h4>
                <p className="mb-4 text-gray-700">
                  Open the Spotify app on your device or go to{" "}
                  <a
                    href="https://open.spotify.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-semibold text-primary hover:underline"
                  >
                    Spotify Web Player
                  </a>
                </p>
                <Image
                  src="/step1.png"
                  alt="Spotify app interface"
                  width={800}
                  height={400}
                  className="w-full rounded-lg border border-gray-300"
                />
              </div>
            </div>

            {/* Step 2 */}
            <div className="flex gap-6 rounded-lg border-2 border-black p-6">
              <div className="flex-shrink-0">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary text-xl font-bold text-white">
                  2
                </div>
              </div>
              <div className="flex-1">
                <h4 className="mb-2 text-xl font-semibold text-black">
                  Navigate to Your Playlist
                </h4>
                <p className="mb-4 text-gray-700">
                  Go to the playlist you want recommendations for
                </p>
                <Image
                  src="/step2.png"
                  alt="Playlist view"
                  width={800}
                  height={400}
                  className="w-full rounded-lg border border-gray-300"
                />
              </div>
            </div>

            {/* Step 3 */}
            <div className="flex gap-6 rounded-lg border-2 border-black p-6">
              <div className="flex-shrink-0">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary text-xl font-bold text-white">
                  3
                </div>
              </div>
              <div className="flex-1">
                <h4 className="mb-2 text-xl font-semibold text-black">
                  Click the Three Dots (•••)
                </h4>
                <p className="mb-4 text-gray-700">
                  Click on the three dots menu button on your playlist
                </p>
                <Image
                  src="/step3.png"
                  alt="Three dots menu"
                  width={800}
                  height={400}
                  className="w-full rounded-lg border border-gray-300"
                />
              </div>
            </div>

            {/* Step 3.5 - Optional */}
            <div className="flex gap-6 rounded-lg border-2 border-primary bg-primary/5 p-6">
              <div className="flex-shrink-0">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white border-2 border-primary text-xl font-bold text-primary">
                  ⚠️
                </div>
              </div>
              <div className="flex-1">
                <h4 className="mb-2 text-xl font-semibold text-black">
                  Make Sure Your Playlist is Public <span className="text-md text-primary">(Important!)</span>
                </h4>
                <p className="mb-4 text-gray-700">
                  In the same three dots menu, look for the option to make your playlist public if it isn't already. Do this by selecting <span className="font-semibold text-black">"Make Public"</span> or <span className="font-semibold text-black">"Add to profile"</span>.
                  <span className="font-semibold text-black"> We can only access public playlists!</span> Don't worry, you can make it private again after using RedditJams!
                </p>
                <Image
                  src="/public-step.png"
                  alt="Make playlist public option"
                  width={800}
                  height={400}
                  className="w-full rounded-lg border border-gray-300"
                />
              </div>
            </div>

            {/* Step 4 */}
            <div className="flex gap-6 rounded-lg border-2 border-black p-6">
              <div className="flex-shrink-0">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary text-xl font-bold text-white">
                  4
                </div>
              </div>
              <div className="flex-1">
                <h4 className="mb-2 text-xl font-semibold text-black">
                  Select "Share" → "Copy Link to Playlist"
                </h4>
                <p className="mb-4 text-gray-700">
                  From the menu, hover over Share and click  <span className="font-semibold text-black"> "Copy link to
                  playlist"</span> 
                </p>
                <Image
                  src="/step4.png"
                  alt="Share menu with copy link option"
                  width={800}
                  height={400}
                  className="w-full rounded-lg border border-gray-300"
                />
              </div>
            </div>

            {/* Step 5 */}
            <div className="flex gap-6 rounded-lg border-2 border-black p-6">
              <div className="flex-shrink-0">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary text-xl font-bold text-white">
                  5
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="mb-2 text-xl font-semibold text-black">
                  Paste the Link Above
                </h4>
                <p className="mb-4 text-gray-700">
                  Paste the copied public playlist link into the input field at the top of this
                  page and click Start!
                </p>
                <div className="rounded-lg bg-primary/10 p-4 overflow-x-auto">
                  <p className="font-mono text-sm text-black break-all">
                    Example: https://open.spotify.com/playlist/3XyDvjoxiae0oWpfJ4kga9
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t-2 border-black bg-black px-4 md:px-8 py-12 text-white">
        <div className="mx-auto max-w-7xl">
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-8 md:gap-24">
            {/* Logo - top on mobile, left on desktop */}
            <div className="flex-shrink-0 hidden md:block">
              <Image
                src="/logo.svg"
                alt="RedditJams Logo"
                width={120}
                height={120}
              />
            </div>

            {/* About, Links, and Creator - equally spaced */}
            <div className="flex flex-col md:flex-row flex-1 md:justify-between gap-8 md:gap-16">
              {/* About */}
              <div className="flex-1">
                <h4 className="mb-4 text-lg font-bold text-primary">About</h4>
                <p className="text-sm text-gray-300 md:max-w-xs">
                  RedditJams is an intelligent music recommendation system that
                  combines Spotify data, Reddit community insights, and AI to help
                  you discover your next favorite songs.
                </p>
              </div>

              {/* Links */}
              <div className="flex-1">
                <h4 className="mb-4 text-lg font-bold text-primary">Links</h4>
                <ul className="space-y-2 text-sm">
                  <li>
                    <a
                      href="https://github.com/HaiderMalikk/RedditJams"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-300 transition-colors hover:text-primary"
                    >
                      Source Code
                    </a>
                  </li>
                  <li>
                    <a
                      href="https://github.com/HaiderMalikk/RedditJams/blob/master/licence"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-300 transition-colors hover:text-primary"
                    >
                      License
                    </a>
                  </li>
                </ul>
              </div>

              {/* Creator */}
              <div className="flex-1">
                <h4 className="mb-4 text-lg font-bold text-primary">Creator</h4>
                <p className="text-sm text-gray-300">
                  Built with by{" "}
                  <a
                    href="https://www.haidercodes.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-white transition-colors hover:text-primary font-semibold"
                  >
                    Haider Malik
                  </a>
                </p>
                <p className="mt-2 text-xs text-gray-400">
                  © 2025 RedditJams. All rights reserved.
                </p>
              </div>
            </div>

            {/* Logo - bottom center on mobile only */}
            <div className="flex justify-center md:hidden mt-8">
              <Image
                src="/logo.svg"
                alt="RedditJams Logo"
                width={120}
                height={120}
              />
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
