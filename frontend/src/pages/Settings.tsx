import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Upload } from "lucide-react";
import { toast } from "sonner";
import { useState } from "react";

const Settings = () => {
  const navigate = useNavigate();
  const [logoFile, setLogoFile] = useState<File | null>(null);

  const handleUpdateBrand = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    if (!user.username) {
      toast.error("Please login first");
      navigate("/dashboard");
      return;
    }

    const formData = new FormData(e.currentTarget);
    
    // API expects: username, brand_details (optional), brand_idea (optional), logo (optional)
    const apiFormData = new FormData();
    apiFormData.append("username", user.username);
    
    const brandDescription = formData.get("brand_description") as string;
    const brandIdea = formData.get("brand_idea") as string;
    
    if (brandDescription) {
      apiFormData.append("brand_details", brandDescription);
    }
    if (brandIdea) {
      apiFormData.append("brand_idea", brandIdea);
    }
    if (logoFile) {
      apiFormData.append("logo", logoFile);
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/user/update_brand", {
        method: "POST",
        body: apiFormData,
      });

      if (response.ok) {
        toast.success("Brand details updated successfully!");
      } else {
        const error = await response.json();
        toast.error(error.detail || "Failed to update brand details");
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
        <div className="max-w-2xl mx-auto space-y-6">
          <div>
            <h1 className="text-3xl font-bold mb-2">Settings</h1>
            <p className="text-muted-foreground">
              Manage your brand information and preferences
            </p>
          </div>

          <Card className="p-6">
            <h3 className="font-semibold text-lg mb-4">Brand Information</h3>
            <form onSubmit={handleUpdateBrand} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="brand_description">Brand Description</Label>
                <Textarea
                  id="brand_description"
                  name="brand_description"
                  placeholder="Tell us about your brand..."
                  rows={4}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="brand_idea">Brand Idea/Mission</Label>
                <Textarea
                  id="brand_idea"
                  name="brand_idea"
                  placeholder="What's your brand vision?"
                  rows={3}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="logo">Update Brand Logo</Label>
                <div className="flex items-center gap-2">
                  <Input
                    id="logo"
                    type="file"
                    accept="image/*"
                    onChange={(e) => setLogoFile(e.target.files?.[0] || null)}
                    className="hidden"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    className="w-full"
                    onClick={() => document.getElementById("logo")?.click()}
                  >
                    <Upload className="w-4 h-4 mr-2" />
                    {logoFile ? logoFile.name : "Upload New Logo"}
                  </Button>
                </div>
              </div>

              <Button type="submit" className="w-full bg-gradient-brand hover:opacity-90">
                Update Brand Details
              </Button>
            </form>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Settings;
