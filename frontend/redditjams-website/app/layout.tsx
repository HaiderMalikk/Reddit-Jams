import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import "./globals.css";
import { Analytics } from "@vercel/analytics/react";

const montserrat = Montserrat({
  variable: "--font-montserrat",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "RedditJams - Discover Music With Reddit",
  description: "Discover trending music and create Spotify playlists from your favorite Reddit communities. Find new songs shared across Reddit's music subreddits. Created by Haider Malik",
  keywords: ["Reddit", "music", "Spotify", "playlist", "discover music", "reddit music", "music discovery"],
  authors: [{ name: "RedditJams" }],
  creator: "RedditJams",
  publisher: "RedditJams",
  openGraph: {
    title: "RedditJams - Discover Music With Reddit",
    description: "Discover trending music and create Spotify playlists from your favorite Reddit communities.",
    url: "https://redditjams.com",
    siteName: "RedditJams",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "RedditJams - Discover Music With Reddit",
    description: "Discover trending music and create Spotify playlists from your favorite Reddit communities.",
    creator: "@redditjams",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  viewport: {
    width: "device-width",
    initialScale: 1,
    maximumScale: 5,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="./favicon.ico" type="image/x-icon" />
      </head>
      <body className={`${montserrat.variable} antialiased`}>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
