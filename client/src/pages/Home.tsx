import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { trpc } from "@/lib/trpc";
import { toast } from "sonner";
import { Loader2, TrendingUp } from "lucide-react";

export default function Home() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const subscribeMutation = trpc.newsletter.subscribe.useMutation();
  const countQuery = trpc.newsletter.getSubscriberCount.useQuery();

  const handleSubscribe = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) {
      toast.error("Please enter a valid email");
      return;
    }

    setLoading(true);
    try {
      await subscribeMutation.mutateAsync({ email });
      toast.success("Welcome! Check your inbox for the next trend.");
      setEmail("");
      // Refresh subscriber count
      countQuery.refetch();
    } catch (error) {
      toast.error("Failed to subscribe. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-white flex flex-col">
      {/* Navigation */}
      <nav className="border-b border-slate-700/50 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-6 h-6 text-emerald-400" />
            <span className="text-lg font-bold">Ahead of the Boom</span>
          </div>
          <div className="text-sm text-slate-400">Trend Intelligence Newsletter</div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-1 flex items-center justify-center px-4 py-16">
        <div className="max-w-2xl w-full">
          {/* Headline */}
          <h1 className="text-5xl md:text-6xl font-bold text-center mb-6 leading-tight">
            See The Next Big Trend Before It Mainstreams.
          </h1>

          {/* Subheading */}
          <p className="text-xl text-slate-300 text-center mb-12 leading-relaxed">
            Every Thursday at 8 AM, we deliver AI-synthesized insights from Reddit, GitHub, and emerging tech communities. Identify macro-trends before they become mainstream.
          </p>

          {/* Email Capture Form */}
          <form onSubmit={handleSubscribe} className="space-y-4 mb-12">
            <div className="flex flex-col sm:flex-row gap-3">
              <Input
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
                className="flex-1 bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 focus:border-emerald-400 focus:ring-emerald-400/20"
              />
              <Button
                type="submit"
                disabled={loading}
                className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-8 py-2 rounded-lg transition-colors"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Subscribing...
                  </>
                ) : (
                  "Subscribe"
                )}
              </Button>
            </div>
            <p className="text-sm text-slate-400 text-center">
              No spam. Unsubscribe anytime.
            </p>
          </form>

          {/* Social Proof */}
          {countQuery.data && (
            <div className="text-center mb-12">
              <div className="inline-block bg-slate-800/50 border border-slate-700 rounded-lg px-6 py-3">
                <p className="text-sm text-slate-400">Joined by</p>
                <p className="text-2xl font-bold text-emerald-400">
                  {countQuery.data.count.toLocaleString()} subscribers
                </p>
              </div>
            </div>
          )}

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 pt-12 border-t border-slate-700/50">
            <div className="text-center">
              <div className="text-3xl mb-2">🔍</div>
              <h3 className="font-semibold mb-2">Deep Research</h3>
              <p className="text-sm text-slate-400">
                AI-powered analysis of trending discussions across platforms
              </p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">⚡</div>
              <h3 className="font-semibold mb-2">Weekly Insights</h3>
              <p className="text-sm text-slate-400">
                Every Thursday: one macro-trend with 3 data-backed points
              </p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">🧠</div>
              <h3 className="font-semibold mb-2">Actionable</h3>
              <p className="text-sm text-slate-400">
                Identify opportunities before the mainstream catches up
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-700/50 bg-slate-950/50 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 py-6 text-center text-sm text-slate-500">
          <p>© 2026 Ahead of the Boom. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
