import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Send, Sparkles, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { Progress } from "@/components/ui/progress";

interface TimelineStep {
  agent: string;
  status: "pending" | "running" | "complete";
  output?: string;
}

interface Result {
  caption: string;
  description: string;
  hashtags: string[];
  image_url: string;      // <-- URL for frontend display
  image_path: string;     // <-- backend local path for publishing
}

const Create = () => {
  const navigate = useNavigate();
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [timeline, setTimeline] = useState<TimelineStep[]>([]);
  const [result, setResult] = useState<Result | null>(null);
  const [progress, setProgress] = useState(0);

  const agents = [
    { name: "WriterAgent", description: "Enhancing your prompt" },
    { name: "Outliner", description: "Creating content structure" },
    { name: "Captioner", description: "Generating caption & hashtags" },
    { name: "Designer", description: "Crafting image prompt" },
    { name: "ImageGenerator", description: "Creating visual" },
  ];

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error("Please enter a creative prompt");
      return;
    }

    const user = JSON.parse(localStorage.getItem("user") || "{}");
    if (!user.username) {
      toast.error("Please login first");
      navigate("/auth");
      return;
    }

    setIsGenerating(true);
    setResult(null);
    setProgress(0);

    const initialTimeline: TimelineStep[] = agents.map((agent) => ({
      agent: agent.name,
      status: "pending" as const,
    }));
    setTimeline(initialTimeline);

    try {
      const formData = new FormData();
      formData.append("user_prompt", prompt);
      formData.append("username", user.username);
      formData.append("context", "{}");

      const response = await fetch("http://127.0.0.1:8000/run_workflow", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        toast.error(error.detail || error.error || "Generation failed");
        return;
      }

      const data = await response.json();
      
      // Update timeline visually
      if (data.timeline && Array.isArray(data.timeline)) {
        let completedCount = 0;
        
        data.timeline.forEach((step: any) => {
          setTimeline((prev) =>
            prev.map((item) => {
              if (item.agent === step.step) {
                completedCount++;
                return { 
                  ...item, 
                  status: "complete" as const, 
                  output: step.enhanced || step.outline || step.caption || step.image_prompt || step.generated_image || ""
                };
              }
              return item;
            })
          );
        });
        
        setProgress((completedCount / agents.length) * 100);
      }

      // Set final result (MINIMAL CHANGE HERE)
      if (data.generated_image && data.caption) {
        setResult({
          caption: typeof data.caption === 'object' ? data.caption.caption || "" : data.caption,
          description: typeof data.caption === 'object' ? data.caption.description || "" : "",
          hashtags: typeof data.caption === 'object' && Array.isArray(data.caption.hashtags)
            ? data.caption.hashtags
            : [],

          // ✔ Use backend URL directly (no file:/// paths)
          image_url: data.generated_image_url,

          // ✔ Keep internal backend path for publishing
          image_path: data.generated_image,
        });

        setProgress(100);
        toast.success("Content generated successfully!");
      }
    } catch (error) {
      toast.error("Network error. Please check your connection.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handlePublish = async () => {
    if (!result) return;

    try {
      const user = JSON.parse(localStorage.getItem("user") || "{}");
      const formData = new FormData();
      formData.append("username", user.username);
      formData.append("image_path", result.image_path); // <-- backend local path
      formData.append("caption_json", JSON.stringify({
        caption: result.caption,
        description: result.description,
        hashtags: result.hashtags,
      }));

      const response = await fetch("http://127.0.0.1:8000/workflow/publish", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        toast.success("Successfully published to Instagram!");
      } else {
        toast.error("Failed to publish to Instagram");
      }
    } catch (error) {
      toast.error("Error publishing to Instagram");
    }
  };

  const handleRegenerate = () => {
    handleGenerate();
  };

  return (
    <div className="min-h-screen bg-gradient-subtle">
      <header className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <Button variant="ghost" onClick={() => navigate("/dashboard")}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto space-y-6">
          <div>
            <h1 className="text-3xl font-bold mb-2">Create Content</h1>
            <p className="text-muted-foreground">
              Describe what you want to create and watch the AI agents work their magic
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Input Section */}
            <Card className="p-6 space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Your Creative Prompt</label>
                <Textarea
                  placeholder="E.g., Create a festive Diwali post showcasing our new product line with warm, celebratory vibes..."
                  rows={6}
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  disabled={isGenerating}
                />
              </div>

              <Button
                className="w-full bg-gradient-brand hover:opacity-90"
                onClick={handleGenerate}
                disabled={isGenerating}
              >
                {isGenerating ? (
                  <>
                    <Sparkles className="w-4 h-4 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4 mr-2" />
                    Generate Content
                  </>
                )}
              </Button>

              {isGenerating && (
                <div className="space-y-2">
                  <Progress value={progress} className="h-2" />
                  <p className="text-xs text-center text-muted-foreground">
                    {Math.round(progress)}% complete
                  </p>
                </div>
              )}
            </Card>

            {/* Timeline Section */}
            <Card className="p-6">
              <h3 className="font-semibold mb-4 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-primary" />
                AI Agent Timeline
              </h3>
              <div className="space-y-3">
                {timeline.map((step, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded-lg border transition-all ${
                      step.status === "running"
                        ? "border-primary bg-primary/5 animate-pulse-glow"
                        : step.status === "complete"
                        ? "border-green-500/50 bg-green-500/5"
                        : "border-border bg-muted/30"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-sm">{step.agent}</span>
                      <span
                        className={`text-xs px-2 py-1 rounded-full ${
                          step.status === "running"
                            ? "bg-primary/20 text-primary"
                            : step.status === "complete"
                            ? "bg-green-500/20 text-green-600"
                            : "bg-muted text-muted-foreground"
                        }`}
                      >
                        {step.status}
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">
                      {agents[idx]?.description}
                    </p>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Result Section */}
          {result && (
            <Card className="p-6 animate-fade-in">
              <h3 className="font-semibold text-lg mb-4">Generated Content</h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <img
                    src={result.image_url}   // <-- loads correctly via backend URL
                    alt="Generated"
                    className="w-full rounded-lg shadow-lg"
                  />
                </div>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-muted-foreground">Caption</label>
                    <p className="mt-1">{result.caption}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-muted-foreground">Description</label>
                    <p className="mt-1 text-sm">{result.description}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-muted-foreground">Hashtags</label>
                    <p className="mt-1 text-sm text-primary">{result.hashtags.join(" ")}</p>
                  </div>
                  <div className="flex gap-2 pt-4">
                    <Button className="flex-1 bg-gradient-brand" onClick={handlePublish}>
                      Publish to Instagram
                    </Button>
                    <Button variant="outline" onClick={handleRegenerate}>
                      <RefreshCw className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </div>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
};

export default Create;
