import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Calendar as CalendarIcon, Plus } from "lucide-react";
import { toast } from "sonner";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { format } from "date-fns";

const Scheduler = () => {
  const navigate = useNavigate();
  const [date, setDate] = useState<Date>();
  const [campaigns, setCampaigns] = useState<any[]>([]);

  const handleCreateCampaign = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const user = JSON.parse(localStorage.getItem("user") || "{}");
    if (!user.username) {
      toast.error("Please login first");
      navigate("/auth");
      return;
    }

    const formData = new FormData(e.currentTarget);
    const festivalName = formData.get("festival_name") as string;
    const extraPrompt = formData.get("extra_prompt") as string;

    // NEW: Read festival time
    const festivalTime = formData.get("festival_time") as string;

    if (!date) {
      toast.error("Please select a festival date");
      return;
    }

    try {
      // Combine date + time (minimal change)
      let finalDate = date;

      if (festivalTime) {
        const [hours, minutes] = festivalTime.split(":").map(Number);
        finalDate = new Date(date);
        finalDate.setHours(hours, minutes, 0, 0);
      }

      const apiFormData = new FormData();
      apiFormData.append("username", user.username);
      apiFormData.append("festival_name", festivalName);
      apiFormData.append("festival_date", finalDate.toISOString()); // ← updated
      if (extraPrompt) {
        apiFormData.append("extra_prompt", extraPrompt);
      }

      const response = await fetch("http://127.0.0.1:8000/scheduler/create", {
        method: "POST",
        body: apiFormData,
      });

      if (response.ok) {
        const data = await response.json();
        toast.success("Campaign scheduled successfully!");
        setCampaigns(prev => [
          ...prev,
          {
            festival_name: festivalName,
            festival_date: finalDate,
            extra_prompt: extraPrompt,
          },
        ]);
        setDate(undefined);
        (e.target as HTMLFormElement).reset();
      } else {
        const error = await response.json();
        toast.error(error.detail || "Failed to schedule campaign");
      }
    } catch (error) {
      toast.error("Network error. Please check your connection.");
    }
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
        <div className="max-w-5xl mx-auto space-y-6">
          <div>
            <h1 className="text-3xl font-bold mb-2">Schedule Campaigns</h1>
            <p className="text-muted-foreground">
              Plan automated content for festivals and special events
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Create Campaign Form */}
            <Card className="p-6">
              <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
                <Plus className="w-5 h-5 text-primary" />
                New Campaign
              </h3>
              <form onSubmit={handleCreateCampaign} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="festival_name">Festival/Event Name</Label>
                  <Input
                    id="festival_name"
                    name="festival_name"
                    placeholder="e.g., Diwali 2024"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label>Festival Date</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        className="w-full justify-start text-left font-normal"
                      >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {date ? format(date, "PPP") : "Pick a date"}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                      <Calendar
                        mode="single"
                        selected={date}
                        onSelect={setDate}
                        initialFocus
                      />
                    </PopoverContent>
                  </Popover>
                  <p className="text-xs text-muted-foreground">
                    Content will be generated 48 hours before this date/time
                  </p>
                </div>

                {/* NEW: Time selector (minimal addition) */}
                <div className="space-y-2">
                  <Label htmlFor="festival_time">Festival Time (Optional)</Label>
                  <Input
                    type="time"
                    id="festival_time"
                    name="festival_time"
                    step="60"
                  />
                  <p className="text-xs text-muted-foreground">
                    If not selected, defaults to 00:00
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="extra_prompt">Campaign Instructions (Optional)</Label>
                  <Textarea
                    id="extra_prompt"
                    name="extra_prompt"
                    placeholder="Any specific instructions for this campaign..."
                    rows={3}
                  />
                </div>

                <Button type="submit" className="w-full bg-gradient-brand hover:opacity-90">
                  Schedule Campaign
                </Button>
              </form>
            </Card>

            {/* Upcoming Campaigns */}
            <Card className="p-6">
              <h3 className="font-semibold text-lg mb-4">Upcoming Campaigns</h3>
              {campaigns.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <CalendarIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>No campaigns scheduled yet</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {campaigns.map((campaign, idx) => (
                    <div key={idx} className="p-4 border rounded-lg">
                      <div className="font-medium">{campaign.festival_name}</div>
                      <div className="text-sm text-muted-foreground mt-1">
                        {format(campaign.festival_date, "PPP")}
                      </div>
                      {campaign.extra_prompt && (
                        <p className="text-xs text-muted-foreground mt-2">
                          {campaign.extra_prompt}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </div>

          {/* Info Card */}
          <Card className="p-6 bg-primary/5 border-primary/20">
            <h4 className="font-semibold mb-2">How It Works</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5" />
                AI generates content 48 hours before the festival date/time
              </li>
              <li className="flex items-start gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5" />
                You receive an approval email with the generated content
              </li>
              <li className="flex items-start gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5" />
                Choose to Publish, Regenerate, or Abort via email links
              </li>
              <li className="flex items-start gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5" />
                Approved content publishes automatically to Instagram
              </li>
            </ul>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Scheduler;
