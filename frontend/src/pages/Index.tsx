import { Button } from "@/components/ui/button";
import { Sparkles, Instagram, Calendar, Zap, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-subtle">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">AI-Powered Instagram Marketing</span>
          </div>
          
          <h1 className="text-6xl md:text-7xl font-bold leading-tight">
            Create Instagram Content
            <span className="block bg-gradient-instagram bg-clip-text text-transparent bg-[length:200%_auto] animate-gradient-shift mt-2">
              10x Faster with AI
            </span>
          </h1>
          
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Multi-agent AI workflow handles everything from concept to caption to posting.
            Schedule campaigns, approve via email, publish automatically.
          </p>

          <div className="flex gap-4 justify-center pt-4">
            <Button 
              size="lg" 
              className="bg-gradient-brand hover:opacity-90 text-lg px-8"
              onClick={() => navigate("/auth")}
            >
              Get Started Free
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
            <Button 
              size="lg" 
              variant="outline"
              className="text-lg px-8"
              onClick={() => navigate("/auth")}
            >
              Sign In
            </Button>
          </div>

          {/* 🔥 Removed trust section: circles + "500+ brands" */}
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">
            Two Powerful Workflows
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8">
            {/* Manual Workflow */}
            <div className="p-8 rounded-2xl bg-card border shadow-card hover:shadow-glow transition-all">
              <div className="w-14 h-14 rounded-xl bg-gradient-brand flex items-center justify-center mb-6">
                <Zap className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Create Now</h3>
              <p className="text-muted-foreground mb-6">
                Interactive workflow with live AI agent timeline. See your content being created in real-time.
              </p>
              <ul className="space-y-3 text-sm">
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-primary" />
                  Writer enhances your prompt
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-primary" />
                  Critic refines the concept
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-primary" />
                  Designer creates image prompt
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-primary" />
                  Generator produces final visual
                </li>
              </ul>
            </div>

            {/* Scheduled Workflow */}
            <div className="p-8 rounded-2xl bg-card border shadow-card hover:shadow-glow transition-all">
              <div className="w-14 h-14 rounded-xl bg-gradient-brand flex items-center justify-center mb-6">
                <Calendar className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Schedule Campaigns</h3>
              <p className="text-muted-foreground mb-6">
                Automated content for festivals and events. Set it and forget it with email approvals.
              </p>
              <ul className="space-y-3 text-sm">
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-accent" />
                  Plan campaigns for key dates
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-accent" />
                  Auto-generate 48h before event
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-accent" />
                  Email approval workflow
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-accent" />
                  One-click publish or regenerate
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto text-center p-12 rounded-2xl bg-gradient-brand text-white">
          <Instagram className="w-16 h-16 mx-auto mb-6 opacity-90" />
          <h2 className="text-4xl font-bold mb-4">
            Ready to Transform Your Instagram Marketing?
          </h2>
          <p className="text-lg mb-8 opacity-90">
            Join hundreds of brands using AI to create stunning content effortlessly.
          </p>
          <Button 
            size="lg" 
            variant="secondary"
            className="text-lg px-8"
            onClick={() => navigate("/auth")}
          >
            Start Creating for Free
            <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Index;
