# Text-to-Video Prompting Reference
> Source: GenHQ — "Prompting 101" presentation

---

## The Template ("Burger Formula")

> Build your prompts like a burger. You need layers!

```
[Medium] + [Shot] + [Angle] + [Movement] + [Focus] + [Subject] + [Lighting] + [Color]
```

---

## 1. Medium

The type and style of the image (e.g. cinematic live action, animates 3D render, video footage, etc.)

### Analog Film
*Organic texture, imperfections, history*

| Medium | Visual Characteristics | Best For |
|---|---|---|
| 8mm / Super 8 Film | Heavy grain, soft focus, flickering light, warm nostalgic colors, jittery frame edges | Memories, indie music videos, home-movie aesthetics |
| 16mm Film | Notable grain, raw/gritty texture, high contrast, documentary-style color | Indie dramas, 70s crime thrillers, raw fashion shoots |
| 35mm Film | Fine grain, rich dynamic range, "creamy" skin tones, classic cinematic depth | Standard Hollywood drama, prestige television, timeless storytelling |
| 70mm / IMAX Film | Crystal clear, immense detail, sweeping scale, minimal grain, ultra-sharp focus | Epic landscapes, space travel, high-budget blockbusters |
| Polaroid / Instant Film | Blown-out highlights, crushed blacks, square 1:1 aspect ratio, chemical color shifts | Retro fashion, dream sequences, "lost" evidence |

### Broadcast & Digital
*High-end 'clean' to retro 'bad'*

| Medium | Visual Characteristics | Best For |
|---|---|---|
| Digital Cinema (Arri/Red) | Ultra-high resolution, clean highlights, perfect color science, no grain | Modern blockbusters, sci-fi, commercial car ads |
| VHS / Camcorder | Tracking lines, color bleeding (chroma smear), 4:3 aspect ratio, magnetic tape hiss | 90s horror, "found footage," lo-fi aesthetic |
| CCTV / Security Cam | Low frame rate, monochrome or green tint, digital timestamps, pixelation | Thrillers, crime scenes, voyeuristic horror |
| GoPro / Action Cam | Fish-eye distortion, high frame rate, extreme wide-angle, hyper-stabilized | Extreme sports, first-person chases, underwater |
| iPhone / Smartphone | Vertical 9:16 aspect ratio, high sharpening, digital depth of field, vivid saturation | Social media content, vlogs, modern "citizen journalism" |

### Animation & Synthetic
*'Impossible' visuals and stylized artistry*

| Medium | Visual Characteristics | Best For |
|---|---|---|
| Unreal Engine 5 / CGI | Global illumination, ray-traced reflections, perfect symmetry, 8k textures | High-fantasy, sci-fi, architectural visualization |
| Stop-Motion Animation | Tactile textures (clay, wood, cloth), 12fps "choppy" movement, thumbprint details | Whimsical tales, dark fairy tales, artistic shorts |
| Anime / Cel Shaded | Bold outlines, flat color planes, dramatic lighting streaks, high saturation | High-octane action, stylized fantasy, cyberpunk |
| 3D Claymation | Squashed and stretched shapes, fingerprints on models, soft matte lighting | Comedic characters, childhood nostalgia |
| Cybernetic Glitch Art | Datamoshing, pixel sorting, neon color frills, fractured frames | Psychological breaks, drug sequences, tech-thrillers |

### Photography & Editorial
*High contrast/res 'frozen' moments*

| Medium | Visual Characteristics | Best For |
|---|---|---|
| Fashion Editorial | High-key lighting, skin retouching, dramatic poses, luxury textures | High-end apparel, perfume ads, "glamour" shots |
| National Geographic Style | Natural light, telephoto compression, hyper-detailed wildlife/textures | Nature documentaries, travel, tribal portraiture |
| Street Photography | Candid movement, high contrast, "Leica" look, accidental focus | Urban life, gritty cityscapes, "slices of life" |

---

## 2. Shot

*The Framing Distance — How close is the subject?*

| Code | Shot Type | Focus |
|---|---|---|
| ECU | Extreme Close-Up | Tiny details / Macro |
| CU | Close-Up | Face / Emotion |
| MCU | Medium Close-Up | Chest up / Dialogue |
| MS | Medium Shot | Waist up / Interaction |
| MFS | Medium Full Shot | Thigh up / The "Cowboy" |
| FS / LS | Full / Long Shot | Entire body / Movement |
| WS | Wide Shot | Character + Environment |
| EWS / ELS | Extreme Wide / Long | Landscape / Scale |

---

## 3. Angle

*The Position of the Camera — Relative to Subject*

| Abbreviation | Full Name | The 'Vibe' / Result |
|---|---|---|
| EL | Eye-Level | Neutral; realistic and grounded |
| LA | Low Angle | Powerful; makes subject look dominant |
| HA | High Angle | Vulnerable; makes subject look small |
| OH | Overhead Shot | Clinical; the 'God-view' from above |
| DA | Dutch Angle | Tense; tilted frame for disorientation |
| POV | Point-of-View | Immersive; seeing through their eyes |
| OTS | Over-the-Shoulder | Connected; used for confrontations/dialogue |

---

## 4. Movement

*In video, you must describe two things:*
- **Movement** — what the subject/environment does
- **Camera** — what the lens does

### Camera Movements

| Movement | Description |
|---|---|
| Static / Locked-Off | The camera does not move. Great for subtle movement (rain, blinking, wind). |
| Pan (Left/Right) | The camera swivels left or right. Great for following action or revealing a landscape. |
| Tilt (Up/Down) | The camera angles up or down. Look up at a skyscraper or down at your feet. |
| Jib Up / Down (Crane) | The camera physically moves vertically through the air. Changes height, not just angle. |
| Push-In (Dolly In) | The camera physically moves forward. Increases intensity or focus. |
| Pull-Out (Dolly Out) | The camera physically moves backward. Great for "reveals" or ending a scene. |
| Truck (Left/Right) | The camera physically moves sideways (sliding). Great for following a walking character side-by-side. |
| Orbit / Arc | The camera circles around the subject. Makes the subject look epic, heroic, or isolated. |
| Zoom | The lens magnifies the image (camera stays still). Note: AI often confuses Zoom and Push-In — Zoom feels flatter and faster. |
| Handheld | Raw and chaotic. Best For: Documentaries or high-stress scenes. |

---

## 5. Focus

*The sharpness of the image*

| Abbreviation | Full Name | The 'Vibe' / Result |
|---|---|---|
| RF | Rack Focus | Redirecting; shifts focus between subjects |
| DF | Deep Focus | Objective; everything in frame is sharp |
| SF | Shallow Focus | Intimate; blurry background (Bokeh) |
| SPD | Split-Field Diopter | Surreal; two separate planes in focus at once |

---

## 6. Subject

*What is happening?* (e.g. the subject is walking, the trees are swaying, the car is driving, etc.)

Free-text description of the scene action. This is the only open ingredient in the template.

---

## 7. Lighting

*Tell your story: Mood, sub-text, and texture*

| Style | Description | Vibe | Best For |
|---|---|---|---|
| Chiaroscuro (High-Contrast) | Extreme shadows & bright highlights | Dramatic, mysterious, moody | Film noir, thriller scenes, dark fantasy |
| Three-Point Lighting | Key, Fill, and Backlight — the "default" studio-quality look | Professional, polished, clean | Character introductions, interviews |
| Motivated Lighting | Mimics a natural source within the scene (lamp, window) | Realistic, organic, grounded | Period dramas, cozy movies |
| Neon Noir (Cyberpunk) | Vibrant artificial colored lights casting harsh shadows | Futuristic, hyper-stylized, electric | Sci-fi cities, club scenes |
| High-Key Lighting | Frame flooded with light, minimal shadows, "airy" image | Upbeat, optimistic, ethereal | Comedies, sitcoms, dream sequences |
| Low-Key Lighting | Dominated by shadow with very few light sources | Supernatural, scary, somber, intimate | Horror movies, tense standoffs |
| Volumetric Lighting ("God Rays") | Beams of light visible through dust, fog, or smoke | Epic, sacred, atmospheric | Ancient ruins, churches, morning forests |
| Color Gels | Colored filters over lights to strongly saturate a specific hue | Saturated, theatrical | Music videos, abstract scenes |
| Rim Lighting / Hair Light | Strong backlight creating a glowing outline around the subject | Glamorous, depth-adding | Silhouettes, product photography |
| Rembrandt Lighting | Small illuminated triangle on the shadowed side of the face | Timeless, painterly | Portraits, period pieces |
| Practical Lighting | In-scene light sources (lamps, candles, monitors, fires) as key motivators | Realistic, naturalistic | Nighttime driving, indoor scenes |
| Haze / Atmospheric | Haze, smoke, or mist illuminated (or darkened) to fill the atmosphere | Dreamlike, eerie | Dystopian worlds, cinematic dream sequences |

---

## 8. Color

*Color Theory — how color tells the story*

| Color Scheme | Description | The Vibe |
|---|---|---|
| Orange & Teal | Opposite colors that make skin tones pop against blue backgrounds | The 'Blockbuster' look, cinematic, professional |
| Monochromatic | Different shades of a single color (e.g. all greens) | Obsessive, dreamlike, or claustrophobic (The Matrix) |
| Analogous | Colors next to each other (e.g. Red, Orange, Yellow) | Harmonious, natural, and comforting |
| Complementary | High-contrast opposites (e.g. Purple and Yellow) | Vibrant, high-energy, and conflicting |

---

## Example Prompts

**Horror / Psychological thriller**
> [Handheld 16mm Raw Footage], [Close-Up] from a [Low Angle]. [Handheld] camera movement with [Shallow Focus]. A protagonist breathing heavily in a flickering hallway. [Low-Key lighting] with a rhythmic strobe effect. [Desaturated] cold blue and grey palette.

**Western**
> [Cinematic Live-Action Film], [Medium Close-Up] [Low Angle] [Static] [Rack Focus] Starting on the metallic, detailed barrel of a cocked revolver in the foreground, then shifting focus to an unsuspecting cowboy standing in the dusty street in the distance. [Hard Motivated] sunlight creating sharp shadows. [Western Sepia] color palette with warm desert tones.

**Film noir**
> [35mm Black and White Film], [Medium Close-Up] with a [Dutch Angle]. [Static camera] and [Deep Focus]. A detective in a trench coat smoking a cigarette under a streetlamp. [Chiaroscuro lighting] with heavy Venetian blind shadows. [Monochromatic] silver-screen palette.

**Post-apocalyptic**
> [Anamorphic Cinematic Film], [Full Shot] at [Eye-Level]. [Tracking Shot] following the movement. [Soft Focus] on the background foliage. A scavenger walking through an overgrown, abandoned city mall. [Motivated natural light]. [Complementary] rusted oranges and vine-leaf greens.

**Sci-fi macro**
> [Macro Photography], [Extreme Close-Up] at [Eye-Level]. [Zoom-In] as a [Rack Focus] shifts from the eyelid to the pupil. A human eye reflecting a glowing holographic map. [Neon Noir lighting] with vibrant cyan and magenta hues. [Lens Flare] from the hologram.

**Epic fantasy/sci-fi landscape**
> [IMAX 70mm Digital Render], [Extreme Wide Shot] [High Angle] [Pan Shot] [Deep Focus] A colossal futuristic citadel nestled between jagged snowy mountain peaks. [Volumetric Lighting] with god rays piercing through a heavy atmosphere. [Analogous] icy blues and slate grey color palette, hyper-detailed textures.

**Sci-fi intimate**
> [Sci-Fi Cinematic], [Close-Up], [Eye-Level], [Static camera], [Shallow Focus], a weary astronaut looking out a spaceship window. [Motivated Lighting] from a glowing control panel, with [Volumetric] starlight beams from window. [Orange and Teal] color palette.
