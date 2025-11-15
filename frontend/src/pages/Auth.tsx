import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Sparkles, Instagram, Upload } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

const Auth = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [logoFile, setLogoFile] = useState<File | null>(null);

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    
    const formData = new FormData(e.currentTarget);

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("user", JSON.stringify(data.profile));
        toast.success("Welcome back!");
        navigate("/dashboard");
      } else {
        const error = await response.json();
        toast.error(error.detail || "Invalid credentials");
      }
    } catch (error) {
      toast.error("Login failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);

    const formData = new FormData(e.currentTarget);
    
    // API expects exact field names: username, password, gmail, insta_id, insta_pw, brand_details, brand_idea, logo
    const apiFormData = new FormData();
    apiFormData.append("username", formData.get("username") as string);
    apiFormData.append("password", formData.get("password") as string);
    apiFormData.append("gmail", formData.get("gmail") as string);
    apiFormData.append("insta_id", formData.get("instagram_username") as string);
    apiFormData.append("insta_pw", formData.get("instagram_password") as string);
    apiFormData.append("brand_details", formData.get("brand_description") as string);
    apiFormData.append("brand_idea", formData.get("brand_idea") as string);
    
    if (logoFile) {
      apiFormData.append("logo", logoFile);
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        body: apiFormData,
      });

      if (response.ok) {
        const data = await response.json();
        toast.success("Account created! Please log in.");
        const loginTab = document.querySelector('[value="login"]') as HTMLElement;
        loginTab?.click();
      } else {
        const error = await response.json();
        toast.error(error.detail || "Registration failed");
      }
    } catch (error) {
      toast.error("Network error. Please check your connection and try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-subtle flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid md:grid-cols-2 gap-8 items-center">
        {/* Hero Section */}
        <div className="space-y-6 text-center md:text-left">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">AI-Powered Instagram Marketing</span>
          </div>
          
          <h1 className="text-5xl font-bold leading-tight">
            Create Stunning
            <span className="block bg-gradient-instagram bg-clip-text text-transparent bg-[length:200%_auto] animate-gradient-shift">
              Instagram Content
            </span>
          </h1>
          
          <p className="text-lg text-muted-foreground">
            Let AI agents handle your creative workflow — from concept to caption to post.
            Schedule campaigns, approve via email, and publish automatically.
          </p>

          <div className="flex items-center gap-4 justify-center md:justify-start pt-4">
            <div className="flex -space-x-2">
              {[1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  className="w-10 h-10 rounded-full bg-gradient-brand border-2 border-background"
                />
              ))}
            </div>
            <div className="text-sm text-muted-foreground">
              <span className="font-semibold text-foreground">500+</span> brands trust our AI
            </div>
          </div>
        </div>

        {/* Auth Card */}
        <Card className="p-6 shadow-card">
          <Tabs defaultValue="login" className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-6">
              <TabsTrigger value="login">Login</TabsTrigger>
              <TabsTrigger value="register">Register</TabsTrigger>
            </TabsList>

            <TabsContent value="login">
              <form onSubmit={handleLogin} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="login-username">Username</Label>
                  <Input
                    id="login-username"
                    name="username"
                    placeholder="Enter your username"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="login-password">Password</Label>
                  <Input
                    id="login-password"
                    name="password"
                    type="password"
                    placeholder="Enter your password"
                    required
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full bg-gradient-brand hover:opacity-90 transition-opacity"
                  disabled={isLoading}
                >
                  {isLoading ? "Logging in..." : "Login"}
                </Button>
              </form>
            </TabsContent>

            <TabsContent value="register">
              <form onSubmit={handleRegister} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="reg-username">Username</Label>
                  <Input
                    id="reg-username"
                    name="username"
                    placeholder="Choose a unique username"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="reg-password">Password</Label>
                  <Input
                    id="reg-password"
                    name="password"
                    type="password"
                    placeholder="Create a password"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="reg-gmail">Gmail Address</Label>
                  <Input
                    id="reg-gmail"
                    name="gmail"
                    type="email"
                    placeholder="your@gmail.com"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="ig-username">Instagram Username</Label>
                  <div className="relative">
                    <Instagram className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                    <Input
                      id="ig-username"
                      name="instagram_username"
                      placeholder="@yourhandle"
                      className="pl-10"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="ig-password">Instagram Password</Label>
                  <Input
                    id="ig-password"
                    name="instagram_password"
                    type="password"
                    placeholder="Instagram password"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="brand-desc">Brand Description</Label>
                  <Textarea
                    id="brand-desc"
                    name="brand_description"
                    placeholder="Tell us about your brand..."
                    rows={3}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="brand-idea">Brand Idea/Mission</Label>
                  <Textarea
                    id="brand-idea"
                    name="brand_idea"
                    placeholder="What's your brand vision?"
                    rows={2}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="logo">Brand Logo</Label>
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
                      {logoFile ? logoFile.name : "Upload Logo"}
                    </Button>
                  </div>
                </div>

                <Button
                  type="submit"
                  className="w-full bg-gradient-brand hover:opacity-90 transition-opacity"
                  disabled={isLoading}
                >
                  {isLoading ? "Creating Account..." : "Create Account"}
                </Button>
              </form>
            </TabsContent>
          </Tabs>
        </Card>
      </div>
    </div>
  );
};

export default Auth;
