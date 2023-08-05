using PerceptualColourMaps
using PerceptualColourMaps: ch2ab, newcolourmapdef
using Printf
using PyPlot
using ColorTypes

#=
Code for generating a set of different colormaps from pre-selected
base colors. Totally based on the code from PerceptualColourMaps
package
=#

function buildMap(
    CM;
    N::Int = 256,
    chromaK::Real = 1.0,
    shift::Real = 0.0,
    reverse::Bool = false,
    diagnostics::Bool = false,
    returnname = false,
    equalize = true,
)
    if uppercase(CM.colourspace) == "LAB"
        CM.colpts[:, 2:3] = chromaK * CM.colpts[:, 2:3]
    end

    # Colour map path is formed via a b-spline in the specified colour space
    Npts = size(CM.colpts, 1)

    if Npts < 2
        println(I)
        error("Number of input points must be 2 or more")
    elseif Npts < CM.splineorder
        error("Spline order is greater than number of data points")
    end

    # Rely on the attribute string to identify if colour map is cyclic.  We may
    # want to construct a colour map that has identical endpoints but do not
    # necessarily want continuity in the slope of the colour map path.
    if occursin("cyclic", lowercase(CM.attributeStr))
        cyclic = true
        labspline = pbspline(CM.colpts', CM.splineorder, N)
    else
        cyclic = false
        labspline = bbspline(CM.colpts', CM.splineorder, N)
    end

    # Apply contrast equalisation with required parameters. Note that sigma is
    # normalised with respect to a colour map of length 256 so that if a short
    # colour map is specified the smoothing that is applied is adjusted to suit.
    CM.sigma = CM.sigma * N / 256
    if equalize
        map = equalisecolourmap(
            CM.colourspace,
            labspline',
            CM.formula,
            CM.W,
            CM.sigma,
            cyclic,
            diagnostics,
        )
    else
        map = labspline'
    end

    # If specified apply a cyclic shift to the colour map
    if shift != 0
        if !occursin("cyclic", lowercase(CM.attributeStr))
            @warn "Colour map shifting being applied to a non-cyclic map"
        end
        map = circshift(map, round(Int, N * shift))
    end

    if reverse
        map = Base.reverse(map, dims = 1)
    end

    # Compute mean chroma of colour map for use in the name construction
    lab = srgb2lab(map)
    meanchroma = sum(sqrt.(sum(lab[:, 2:3] .^ 2, dims = 2))) / N

    # Construct lightness range description
    if uppercase(CM.colourspace) == "LAB"  # Use the control points
        L = CM.colpts[:, 1]
    else  # For RGB use the converted CIELAB values
        L = round.(lab[:, 1])
    end
    minL = minimum(L)
    maxL = maximum(L)

    if minL == maxL     # Isoluminant
        LStr = @sprintf("%d", minL)

    elseif L[1] == maxL && (
        occursin("diverging", lowercase(CM.attributeStr)) ||
        occursin("linear", lowercase(CM.attributeStr))
    )
        LStr = @sprintf("%d-%d", maxL, minL)
    else
        LStr = @sprintf("%d-%d", minL, maxL)
    end

    # Build overall colour map name
    name = @sprintf(
        "%s_%s_%s_c%d_n%d",
        CM.attributeStr,
        CM.hueStr,
        LStr,
        Int(round(meanchroma)),
        N
    )

    if shift != 0
        name = @sprintf("%s_s%d", name, round(Int, shift * 100))
    end

    if reverse
        name = @sprintf("%s_r", name)
    end

    # Build an array of ColorTypes.RGB values to return
    rgbmap = Array{ColorTypes.RGBA{Float64}}(undef, N)
    for i = 1:N
        rgbmap[i] = ColorTypes.RGBA(map[i, 1], map[i, 2], map[i, 3], 1.0)
    end

    if returnname
        return rgbmap, name, CM.desc
    else
        return rgbmap
    end
end

# define the base colors
base_colors = Dict(
    "mnfred" => [157 13 21] / 255.0,
    "blue" => [68 114 196] / 255.0,
    "darkpurple" => [86 71 148] / 255.0,
    "darkyellow" => [255 192 0] / 255.0,
    "orange" => [237 125 49] / 255.0,
    "green" => [112 173 71] / 255.0,
)

function saveCPT(cm, fname, N = 256)
    # saves the generated colormap to CPT format,
    # readable by python
    cmap = ColorMap(cm)
    b = Int.(round.(cmap(0.0) .* 255))[1:3]
    f = Int.(round.(cmap(1.0) .* 255))[1:3]
    na = [0, 0, 0]
    vals = collect(range(0.0, 1.0, length = N))
    cols =
        Int.(
            round.(
                cmap(collect(range(0.0, 1.0, length = 256)))[:, 1:3] * 255.0,
            ),
        )
    arr = [vals[1:end-1] cols[1:end-1, :] vals[2:end] cols[2:end, :]]
    open(fname, "w") do io
        println(io, "# COLOR_MODEL = RGB")
        for row in eachrow(arr)
            println(io, @sprintf("%e %3d %3d %3d %e %3d %3d %3d", row...))
        end
        println(
            io,
            @sprintf(
                "B %3d %3d %3d\nF %3d %3d %3d\nN %3d %3d %3d",
                b...,
                f...,
                na...
            )
        )
    end
end

function showMap(mymap; cyclic = false)
    clf()
    if cyclic
        sr, alpha = circlesineramp()
        imshow(sr, cmap = ColorMap(mymap))
    else
        sr = sineramp()
        imshow(sr, cmap = ColorMap(mymap), aspect = 0.2)
    end
    axis("off")
    gcf()
end
#---
# classical hot colormap, slightly adjusted to university colors
quanthot = newcolourmapdef(
    desc = "quant-hot",
    hueStr = "quanthot",
    attributeStr = "linear",
    colourspace = "RGB",
    colpts = [
        0.0 0.0 0.0
        base_colors["mnfred"]
        1.0 0.15 0.0
        base_colors["orange"]
        base_colors["darkyellow"]
        1.0 1.0 1.0
    ],
    splineorder = 2,
    formula = "CIE76",
    W = [1, 0, 0],
    sigma = 0,
)
#---
# derivative of "parula-like" colormap from PerceptualColourMaps
# adjusted to university colors
quantparrot = newcolourmapdef(
    desc = "quant-parrot",
    attributeStr = "linear",
    hueStr = "quantparrot",
    colourspace = "LAB",
    colpts = [
        20 0 0
        srgb2lab(base_colors["blue"])
        srgb2lab(base_colors["green"])
        srgb2lab(base_colors["darkyellow"])
        95 -21 92
    ],
    splineorder = 2,
    formula = "CIE76",
    W = [1, 0, 0],
    sigma = 10,
)

#---
# perceptually unifrom colormap going from
# blue to yellow in the LAB colorspace
# visually reminds plasma

function rgb2lch(rgb)
    l, a, b = srgb2lab(rgb)
    lch = [l, sqrt(a^2 + b^2), rad2deg(atan(b, a))]
    return lch
end

function norm_range(l, newmin, newmax)
    if length(l) > 1
        l .-= minimum(l)
        l ./= maximum(l)
        l .*= (newmax - newmin)
        l .+= newmin
    end
    return l
end

# Map with linear decreasing lightness, increasing chroma to blue.
# Precompute a spiral of increasing chroma down through Lab space
nsteps = 12
# starting from hue of yellow base color
ang1 = rgb2lch(base_colors["darkyellow"])[3]
# going to the hue of blue base color
ang2 = rgb2lch(base_colors["blue"])[3] + 20.0
# Linearly interpolate hue angle
ang = range(ang1, stop = ang2, length = nsteps)

# Interpolate chroma but use a 'gamma' of 0.5 to keep the colours more saturated.
sat1 = 0;
sat2 = 80;
sat = (range(sat1, stop = sat2, length = nsteps) / sat2) .^ 0.5 * sat2

l1 = 100;
l2 = 15;        # Linearly interpoate lightness
l = range(l1, stop = l2, length = nsteps) .^ 1.0
l = norm_range(l, l2, l1)
colptarray = zeros(nsteps, 3)
for n = 1:nsteps
    colptarray[n, :] = [l[n] ch2ab(sat[n], ang[n])]
end

quantplasma = newcolourmapdef(
    desc = "quant-plasma",
    attributeStr = "linear",
    hueStr = "quantplasma",
    colourspace = "LAB",
    colpts = colptarray[end:-1:1, :],
    splineorder = 2,
    formula = "CIE76",
    W = [1, 0, 0],
    sigma = 0,
)
#---
# simple diverging colormap

quantcoolwarm = newcolourmapdef(
    desc = "quant-coolwarm",
    attributeStr = "diverging",
    hueStr = "quantcoolwarm",
    colourspace = "LAB",
    colpts = [
        40 ch2ab(83, rgb2lch(base_colors["blue"])[3])
        95 0 0
        40 ch2ab(83, rgb2lch(base_colors["mnfred"])[3])
    ],
    splineorder = 2,
    formula = "CIE76",
    W = [1, 0, 0],
    sigma = 10,
)

#---
# define helper functions needed to linearly interpolate
# colors in the RGB space
function genCoefs(positions)
    K = 1
    coefs = []
    totlen = positions[end]
    push!(
        coefs,
        [
            collect(range(0.0, length = positions[1]))[end:-1:1]...
            zeros(totlen - positions[1])
        ],
    )
    for i = 1:length(positions)-1
        if i > 1
            prev = positions[i-1]
        else
            prev = 0
        end
        push!(
            coefs,
            [
                zeros(prev)...
                norm_range(
                    collect(range(0.0, length = positions[i] - prev)),
                    0.0,
                    1.0,
                )...
                norm_range(
                    collect(
                        range(0.0, length = positions[i+1] - positions[i]),
                    )[end:-1:1],
                    0.0,
                    1.0,
                )...
                zeros(totlen - positions[i+1])
            ],
        )
    end
    push!(
        coefs,
        [
            zeros(positions[end-1])...
            collect(range(0.0, length = totlen - positions[end-1]))...
        ],
    )
    coefs = Base.map(x -> norm_range(x, 0.0, 1.0), coefs)
    return coefs
end

function interpolateRGB(colors, positions)
    #=
    colors - colors to be interpolated
    positions - positions of color changes, N-1 for N colors
    0 - 100% C1
    P1 - 100% C2
    P2 - 100% C3
    ...
    P_N - 100%
    =#
    coefs = genCoefs(positions)
    res = zeros(coefs[1] |> length, 3)
    for (color, coef) in zip(colors, coefs)
        res += color .* coef
    end
    return res
end


#---
# simple black-white-red colormap, interpolated in RGB space
# not perceptually uniiform
npoints = 105
start = base_colors["blue"]
center = [0.95 0.95 0.95] .* 1.0
stop = base_colors["mnfred"]
coef1 = [collect(range(0.0, length = npoints ÷ 2))[end:-1:1]... zeros(
    npoints ÷ 2,
)...]
K = 0.7
coef1 .^= K
coef1 = norm_range(coef1, 0.0, 1.0)
coef2 = [zeros(npoints ÷ 2)... collect(range(0.0, length = npoints ÷ 2))...]
coef2 .^= K

coef2 = norm_range(coef2, 0.0, 1.0)
cpoints =
    (start .* coef1') .+ (stop .* coef2') .+
    (center .* (1.0 .- coef1 .- coef2)')


quantbwr = newcolourmapdef(
    desc = "quant-bwr",
    attributeStr = "diverging",
    hueStr = "quantbwr",
    colourspace = "RGB",
    colpts = cpoints,
    splineorder = 2,
    formula = "CIE76",
    W = [0, 0, 0], # disable "uniformization"
    sigma = 0,
)

#---
# jet-like colormap, obtained by interpolating base colors
# in RGB space, not perceptually uniform

jetcolors = [
    base_colors[c] for
    c in ["darkpurple", "blue", "green", "darkyellow", "orange", "mnfred"]
]
cpoints = interpolateRGB(jetcolors |> values, [6, 12, 18, 24, 30])
quantjet = newcolourmapdef(
    desc = "",
    attributeStr = "linear",
    hueStr = "quantjet",
    colourspace = "RGB",
    colpts = cpoints,
    splineorder = 2,
    formula = "CIE76",
    W = [0, 0, 0],
    sigma = 0.0,
)
#---
# jet-like colormap, obtained by interpolating base colors
# in RGB space, perc. uniform
quantjetuniform = newcolourmapdef(
    desc = "",
    attributeStr = "linear",
    hueStr = "quantjetuniform",
    colourspace = "RGB",
    colpts = cpoints,
    splineorder = 2,
    formula = "CIE76",
    W = [1, 0, 0],
    sigma = 0.0,
)

#---
# jet-like colormap, obtained by interpolating base colors
# in RGB space, perc. uniform
cyclic_jetcolors = [
    base_colors[c] for c in [
        "darkpurple",
        "blue",
        "green",
        "darkyellow",
        "orange",
        "mnfred",
        "darkpurple",
    ]
]
cyclic_cpoints =
    interpolateRGB(cyclic_jetcolors |> values, [8, 14, 22, 28, 34, 40])

quantcyclicjet = newcolourmapdef(
    desc = "",
    attributeStr = "cyclic",
    hueStr = "quantcyclicjet",
    colourspace = "RGB",
    colpts = cyclic_cpoints,
    splineorder = 5,
    formula = "CIE76",
    W = [0.0, 0, 0],
    sigma = 0.0,
)

#showMap(buildMap(quantcyclicjet, shift=0.0), cyclic=true)

#---
# iterate over all defined colormaps and save them to CPT
for mapdef in [
    quantbwr,
    quanthot,
    quantparrot,
    quantplasma,
    quantcoolwarm,
    quantjetuniform,
    quantjet,
    quantcyclicjet,
]
    mymap, name = buildMap(mapdef, returnname = true)
    saveCPT(mymap, "$(name).cpt")
end



#---
#generate linear colormaps, going each of the base colors to white

for (idx, (color, rgb)) in enumerate(base_colors)
    mymapdef = newcolourmapdef(
        desc = "Grey scale",
        hueStr = "$(color)_white",
        attributeStr = "linear",
        colourspace = "LAB",
        colpts = [
                  [40 srgb2lab(rgb)[2:end]...]
                  100 0 0],
        splineorder = 2,
        formula = "CIE76",
        W = [1, 0, 0],
        sigma = 0,
    )


    mymap, name = buildMap(mymapdef, returnname = true)
    saveCPT(mymap, "$(name).cpt")
end

# and from each of the base colors to black
for (idx, (color, rgb)) in enumerate(base_colors)
    mymapdef = newcolourmapdef(
        desc = "Grey scale",
        hueStr = "black_$(color)",
        attributeStr = "linear",
        colourspace = "LAB",
        colpts = [
            0 0 0
            [70 srgb2lab(rgb)[2:end]...]
        ],
        splineorder = 2,
        formula = "CIE76",
        W = [1, 0, 0],
        sigma = 0,
    )

    mymap, name = buildMap(mymapdef, returnname = true)
    saveCPT(mymap, "$(name).cpt")

end
