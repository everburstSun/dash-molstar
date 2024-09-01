#### cartoon:
    sizeFactor: float;  # Factor to scale the size of the cartoon representation.
    visuals: list (available values are "polymer-trace", "polymer-gap", "nucleotide-ring", "nucleotide-block", "direction-wedge");  # List of visual elements to include in the cartoon representation.
    bumpFrequency: float;  # Frequency of the bump mapping, affecting surface texture.
    unitKinds: list (available values are "spheres", "gaussians", "atomic");  # Types of units used in the representation.
    includeParent: bool;  # Whether to include the parent structure in the representation.
    doubleSided: bool;  # If true, renders both sides of the polygons.
    flipSided: bool;  # If true, flips the normal direction of the polygons.
    flatShaded: bool;  # If true, enables flat shading (no smoothing between polygons).
    ignoreLight: bool;  # If true, the representation will not be affected by the scene's lighting.
    xrayShaded: bool;  # If true, applies an X-ray shading effect to the representation.
    transparentBackfaces: string;  # Determines how transparent backfaces are rendered.
    bumpAmplitude: float;  # Amplitude of the bump mapping, affecting the depth of surface texture.
    alpha: float;  # Transparency level of the representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest");  # Quality level of the representation.
    material: dict;  # Material properties of the cartoon representation.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict;  # Clipping properties for the representation.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  # Type of the clipping object.
            invert: any;  # Whether to invert the clipping region.
            position: any;  # Position of the clipping object.
            rotation: any;  # Rotation of the clipping object.
            scale: any;  # Scale of the clipping object.
    instanceGranularity: bool;  # If true, enables granularity at the instance level.
    radialSegments: float;  # Number of radial segments used in tubular representations.
    detail: float;  # Level of detail in the representation.
    aspectRatio: float;  # Aspect ratio of the cartoon elements.
    arrowFactor: float;  # Factor affecting the size of arrows in directional representations.
    tubularHelices: bool;  # If true, renders helices as tubular structures.
    helixProfile: string (available values are "square", "elliptical", "rounded");  # Profile shape of helices.
    linearSegments: float;  # Number of linear segments used in the representation.
backbone:
    sizeAspectRatio: float;  # Aspect ratio of the backbone elements.
    visuals: list (available values are "polymer-gap", "polymer-backbone-cylinder", "polymer-backbone-sphere");  # List of visual elements to include in the backbone representation.
    bumpFrequency: float;  # Frequency of the bump mapping, affecting surface texture.
    sizeFactor: float;  # Factor to scale the size of the backbone representation.
    radialSegments: float;  # Number of radial segments used in tubular representations.
    unitKinds: list (available values are "spheres", "gaussians", "atomic");  # Types of units used in the representation.
    includeParent: bool;  # Whether to include the parent structure in the representation.
    doubleSided: bool;  # If true, renders both sides of the polygons.
    flipSided: bool;  # If true, flips the normal direction of the polygons.
    flatShaded: bool;  # If true, enables flat shading (no smoothing between polygons).
    ignoreLight: bool;  # If true, the representation will not be affected by the scene's lighting.
    xrayShaded: bool;  # If true, applies an X-ray shading effect to the representation.
    transparentBackfaces: string;  # Determines how transparent backfaces are rendered.
    bumpAmplitude: float;  # Amplitude of the bump mapping, affecting the depth of surface texture.
    alpha: float;  # Transparency level of the representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest");  # Quality level of the representation.
    material: dict;  # Material properties of the backbone representation.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict;  # Clipping properties for the representation.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  # Type of the clipping object.
            invert: any;  # Whether to invert the clipping region.
            position: any;  # Position of the clipping object.
            rotation: any;  # Rotation of the clipping object.
            scale: any;  # Scale of the clipping object.
    instanceGranularity: bool;  # If true, enables granularity at the instance level.
    tryUseImpostor: bool;  # If true, attempts to use impostor rendering for improved performance.
    solidInterior: bool;  # If true, ensures the interior of the backbone elements is solid.
    detail: float;  # Level of detail in the representation.
ball-and-stick:
    includeParent: bool;  # Whether to include the parent structure in the representation.
    unitKinds: list (available values are "spheres", "gaussians", "atomic");  # Types of units used in the representation.
    sizeFactor: float;  # Factor to scale the size of the ball-and-stick representation.
    sizeAspectRatio: float;  # Aspect ratio of the ball-and-stick elements.
    visuals: list (available values are "element-sphere", "intra-bond", "inter-bond");  # List of visual elements to include in the ball-and-stick representation.
    bumpFrequency: float;  # Frequency of the bump mapping, affecting surface texture.
    tryUseImpostor: bool;  # If true, attempts to use impostor rendering for improved performance.
    adjustCylinderLength: bool;  # If true, adjusts the cylinder length to better fit bond distances.
    includeTypes: list (available values are "covalent", "metal-coordination", "hydrogen-bond", "disulfide", "aromatic", "computed");  # Types of bonds to include in the representation.
    excludeTypes: list (available values are "covalent", "metal-coordination", "hydrogen-bond", "disulfide", "aromatic", "computed");  # Types of bonds to exclude from the representation.
    ignoreHydrogens: bool;  # If true, ignores hydrogen atoms in the representation.
    ignoreHydrogensVariant: string (available values are "all", "non-polar");  # Determines which hydrogen atoms to ignore based on type.
    aromaticBonds: bool;  # If true, emphasizes aromatic bonds in the representation.
    multipleBonds: string (available values are "offset", "off", "symmetric");  # Style for rendering multiple bonds.
    linkScale: float;  # Scale factor for the size of bonds in the representation.
    linkSpacing: float;  # Spacing between bonds, particularly for multiple bonds.
    linkCap: bool;  # If true, adds caps to the ends of bonds.
    aromaticScale: float;  # Scale factor for aromatic bonds.
    aromaticSpacing: float;  # Spacing between segments in aromatic bonds.
    aromaticDashCount: float;  # Number of dashes used for representing aromatic bonds.
    dashCount: float;  # Number of dashes used in dashed bonds.
    dashScale: float;  # Scale factor for the size of dashes in dashed bonds.
    dashCap: bool;  # If true, adds caps to the ends of dashed bonds.
    stubCap: bool;  # If true, adds caps to the ends of stub bonds (short bonds).
    radialSegments: float;  # Number of radial segments used in tubular representations.
    doubleSided: bool;  # If true, renders both sides of the polygons.
    ignoreLight: bool;  # If true, the representation will not be affected by the scene's lighting.
    xrayShaded: bool;  # If true, applies an X-ray shading effect to the representation.
    transparentBackfaces: string;  # Determines how transparent backfaces are rendered.
    solidInterior: bool;  # If true, ensures the interior of the bonds and atoms is solid.
    bumpAmplitude: float;  # Amplitude of the bump mapping, affecting the depth of surface texture.
    alpha: float;  # Transparency level of the representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest");  # Quality level of the representation.
    material: dict;  # Material properties of the ball-and-stick representation.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict;  # Clipping properties for the representation.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  # Type of the clipping object.
            invert: any;  # Whether to invert the clipping region.
            position: any;  # Position of the clipping object.
            rotation: any;  # Rotation of the clipping object.
            scale: any;  # Scale of the clipping object.
    instanceGranularity: bool;  # If true, enables granularity at the instance level.
    flipSided: bool;  # If true, flips the normal direction of the polygons.
    flatShaded: bool;  # If true, enables flat shading (no smoothing between polygons).
    traceOnly: bool;  # If true, only traces the backbone without rendering atoms.
    detail: float;  # Level of detail in the representation.
carbohydrate:
    visuals: list (available values are "carbohydrate-symbol", "carbohydrate-link", "carbohydrate-terminal-link");  # The different visual elements to include in the carbohydrate representation.
    bumpFrequency: float;  # Frequency of bump mapping, affecting the texture of the surface.
    terminalLinkSizeFactor: float;  # Size scaling factor for terminal carbohydrate links.
    linkScale: float;  # Scale factor for the size of carbohydrate links.
    linkSpacing: float;  # Spacing between carbohydrate links.
    linkCap: bool;  # If true, adds caps to the ends of carbohydrate links.
    aromaticScale: float;  # Scale factor for aromatic features in the carbohydrate structure.
    aromaticSpacing: float;  # Spacing between segments in aromatic features.
    aromaticDashCount: float;  # Number of dashes used for representing aromatic bonds.
    dashCount: float;  # Number of dashes used in dashed links.
    dashScale: float;  # Scale factor for the size of dashes in dashed links.
    dashCap: bool;  # If true, adds caps to the ends of dashed links.
    stubCap: bool;  # If true, adds caps to the ends of stub links (short links).
    radialSegments: float;  # Number of radial segments used in tubular representations of links.
    unitKinds: list (available values are "spheres", "gaussians", "atomic");  # Types of units used in the representation.
    includeParent: bool;  # Whether to include the parent structure in the representation.
    doubleSided: bool;  # If true, renders both sides of the polygons.
    flipSided: bool;  # If true, flips the normal direction of the polygons.
    flatShaded: bool;  # If true, enables flat shading (no smoothing between polygons).
    ignoreLight: bool;  # If true, the representation will not be affected by the scene's lighting.
    xrayShaded: bool;  # If true, applies an X-ray shading effect to the representation.
    transparentBackfaces: string;  # Determines how transparent backfaces are rendered.
    bumpAmplitude: float;  # Amplitude of the bump mapping, affecting the depth of surface texture.
    alpha: float;  # Transparency level of the representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest");  # Quality level of the representation.
    material: dict;  # Material properties of the carbohydrate representation.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict;  # Clipping properties for the representation.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  # Type of the clipping object.
            invert: any;  # Whether to invert the clipping region.
            position: any;  # Position of the clipping object.
            rotation: any;  # Rotation of the clipping object.
            scale: any;  # Scale of the clipping object.
    instanceGranularity: bool;  # If true, enables granularity at the instance level.
    linkSizeFactor: float;  # Size scaling factor for carbohydrate links.
    detail: float;  # Level of detail in the representation.
    sizeFactor: float;  # Overall size scaling factor for the carbohydrate representation.
ellipsoid:
    includeParent: bool;  # Whether to include the parent structure in the representation.
    adjustCylinderLength: bool;  # If true, adjusts the length of cylinders to better fit the ellipsoid shape.
    unitKinds: list (available values are "spheres", "gaussians", "atomic");  # Types of units used in the representation.
    sizeFactor: float;  # Overall size scaling factor for the ellipsoid representation.
    sizeAspectRatio: float;  # Aspect ratio for scaling the size of the ellipsoids.
    linkCap: bool;  # If true, adds caps to the ends of bonds or links.
    visuals: list (available values are "intra-bond", "inter-bond", "ellipsoid-mesh");  # The different visual elements to include in the ellipsoid representation.
    bumpFrequency: float;  # Frequency of bump mapping, affecting the texture of the surface.
    tryUseImpostor: bool;  # If true, attempts to use impostors for rendering performance optimization.
    includeTypes: list (available values are "covalent", "metal-coordination", "hydrogen-bond", "disulfide", "aromatic", "computed");  # Types of bonds or interactions to include.
    excludeTypes: list (available values are "covalent", "metal-coordination", "hydrogen-bond", "disulfide", "aromatic", "computed");  # Types of bonds or interactions to exclude.
    ignoreHydrogens: bool;  # If true, hydrogen atoms are ignored in the representation.
    ignoreHydrogensVariant: string (available values are "all", "non-polar");  # Specifies which hydrogen atoms to ignore.
    aromaticBonds: bool;  # If true, renders aromatic bonds differently.
    multipleBonds: string (available values are "offset", "off", "symmetric");  # Defines how to represent multiple bonds.
    linkScale: float;  # Scale factor for the size of links.
    linkSpacing: float;  # Spacing between bonds or links.
    aromaticScale: float;  # Scale factor for aromatic bonds or features.
    aromaticSpacing: float;  # Spacing between segments in aromatic features.
    aromaticDashCount: float;  # Number of dashes used for representing aromatic bonds.
    dashCount: float;  # Number of dashes used in dashed links.
    dashScale: float;  # Scale factor for the size of dashes in dashed links.
    dashCap: bool;  # If true, adds caps to the ends of dashed links.
    stubCap: bool;  # If true, adds caps to the ends of stub links (short links).
    radialSegments: float;  # Number of radial segments used in tubular representations of links.
    doubleSided: bool;  # If true, renders both sides of the polygons.
    ignoreLight: bool;  # If true, the representation will not be affected by the scene's lighting.
    xrayShaded: bool;  # If true, applies an X-ray shading effect to the representation.
    transparentBackfaces: string;  # Determines how transparent backfaces are rendered.
    solidInterior: bool;  # If true, renders the interior of the ellipsoid as solid.
    bumpAmplitude: float;  # Amplitude of the bump mapping, affecting the depth of surface texture.
    alpha: float;  # Transparency level of the representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest");  # Quality level of the representation.
    material: dict;  # Material properties of the ellipsoid representation.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict;  # Clipping properties for the representation.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  # Type of the clipping object.
            invert: any;  # Whether to invert the clipping region.
            position: any;  # Position of the clipping object.
            rotation: any;  # Rotation of the clipping object.
            scale: any;  # Scale of the clipping object.
    instanceGranularity: bool;  # If true, enables granularity at the instance level.
    flipSided: bool;  # If true, flips the normal direction of the polygons.
    flatShaded: bool;  # If true, enables flat shading (no smoothing between polygons).
    detail: float;  # Level of detail in the representation.
gaussian-surface:
    visuals: list (available values are "gaussian-surface-mesh", "structure-gaussian-surface-mesh", "gaussian-surface-wireframe");  # The different visual elements to include in the Gaussian surface representation.
    bumpFrequency: float;  # Frequency of bump mapping, affecting the texture of the surface.
    sizeFactor: float;  # Overall size scaling factor for the Gaussian surface representation.
    lineSizeAttenuation: bool;  # If true, enables attenuation of line size based on distance.
    ignoreHydrogens: bool;  # If true, hydrogen atoms are ignored in the representation.
    ignoreHydrogensVariant: string (available values are "all", "non-polar");  # Specifies which hydrogen atoms to ignore.
    includeParent: bool;  # Whether to include the parent structure in the representation.
    traceOnly: bool;  # If true, the representation only traces the backbone or main chain.
    resolution: float;  # The resolution of the Gaussian surface, affecting the level of detail.
    radiusOffset: float;  # Offset applied to the atomic radii in the surface calculation.
    smoothness: float;  # The smoothness of the Gaussian surface, affecting how smooth or jagged it appears.
    unitKinds: list (available values are "spheres", "gaussians", "atomic");  # Types of units used in the representation.
    alpha: float;  # Transparency level of the representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest");  # Quality level of the representation.
    material: dict;  # Material properties of the Gaussian surface representation.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict;  # Clipping properties for the representation.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  # Type of the clipping object.
            invert: any;  # Whether to invert the clipping region.
            position: any;  # Position of the clipping object.
            rotation: any;  # Rotation of the clipping object.
            scale: any;  # Scale of the clipping object.
    instanceGranularity: bool;  # If true, enables granularity at the instance level.
    tryUseGpu: bool;  # If true, attempts to use GPU acceleration for rendering the Gaussian surface.
    smoothColors: mapped;  # Determines how colors are smoothed across the surface.
        auto: default;  # Automatically determines whether to smooth colors.
        on: dict;  # Enables color smoothing with specific parameters.
            resolutionFactor: float;  # Resolution factor for color smoothing.
            sampleStride: float;  # Stride for sampling during color smoothing.
        off: default;  # Disables color smoothing.
    doubleSided: bool;  # If true, renders both sides of the polygons.
    flipSided: bool;  # If true, flips the normal direction of the polygons.
    flatShaded: bool;  # If true, enables flat shading (no smoothing between polygons).
    ignoreLight: bool;  # If true, the representation will not be affected by the scene's lighting.
    xrayShaded: bool;  # If true, applies an X-ray shading effect to the representation.
    transparentBackfaces: string;  # Determines how transparent backfaces are rendered.
    bumpAmplitude: float;  # Amplitude of the bump mapping, affecting the depth of surface texture.
gaussian-volume:
    jumpLength: float;  # The length of jumps within the Gaussian volume representation.
    visuals: list (available values are "gaussian-volume", "units-gaussian-volume");  # The visual elements to include in the Gaussian volume representation.
    ignoreHydrogens: bool;  # If true, hydrogen atoms are ignored in the representation.
    ignoreHydrogensVariant: string (available values are "all", "non-polar");  # Specifies which hydrogen atoms to ignore.
    includeParent: bool;  # Whether to include the parent structure in the representation.
    traceOnly: bool;  # If true, the representation only traces the backbone or main chain.
    resolution: float;  # The resolution of the Gaussian volume, affecting the level of detail.
    radiusOffset: float;  # Offset applied to the atomic radii in the volume calculation.
    smoothness: float;  # The smoothness of the Gaussian volume, affecting how smooth or jagged it appears.
    unitKinds: list (available values are "spheres", "gaussians", "atomic");  # Types of units used in the representation.
    ignoreLight: bool;  # If true, the representation will not be affected by the scene's lighting.
    xrayShaded: bool;  # If true, applies an X-ray shading effect to the representation.
    controlPoints: LineGraph;  # Defines control points for custom adjustments within the volume.
    stepsPerCell: float;  # Number of steps per cell, affecting the resolution of the volume grid.
    alpha: float;  # Transparency level of the representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest");  # Quality level of the representation.
    material: dict;  # Material properties of the Gaussian volume representation.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict;  # Clipping properties for the representation.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  # Type of the clipping object.
            invert: any;  # Whether to invert the clipping region.
            position: any;  # Position of the clipping object.
            rotation: any;  # Rotation of the clipping object.
            scale: any;  # Scale of the clipping object.
    instanceGranularity: bool;  # If true, enables granularity at the instance level.
label:
    visuals: list (available values are "label-text");  # The visual elements to include in the label representation.
    background: bool;  # If true, a background is rendered behind the label text.
    backgroundMargin: float;  # The margin size around the label background.
    backgroundColor: Color;  # The color of the label background.
    backgroundOpacity: float;  # The opacity level of the label background.
    borderWidth: float;  # The width of the border around the label.
    level: string (available values are "element", "residue", "chain");  # The level at which the label is applied (e.g., element, residue, or chain).
    chainScale: float;  # Scaling factor for labels at the chain level.
    residueScale: float;  # Scaling factor for labels at the residue level.
    elementScale: float;  # Scaling factor for labels at the element level.
    unitKinds: list (available values are "spheres", "gaussians", "atomic");  # Types of units used in the representation.
    includeParent: bool;  # Whether to include the parent structure in the representation.
    sizeFactor: float;  # Factor by which to scale the label size.
    borderColor: Color;  # The color of the border around the label.
    offsetX: float;  # The X-axis offset for the label position.
    offsetY: float;  # The Y-axis offset for the label position.
    offsetZ: float;  # The Z-axis offset for the label position.
    tether: bool;  # If true, a tether is drawn from the label to the structure.
    tetherLength: float;  # Length of the tether connecting the label to the structure.
    tetherBaseWidth: float;  # Base width of the tether.
    attachment: string (available values are "bottom-left", "bottom-center", "bottom-right", "middle-left", "middle-center", "middle-right", "top-left", "top-center", "top-right");  # The attachment point of the label relative to the text.
    fontFamily: string (from FontFamily);  # Font family used for the label text.
    fontQuality: int;  # Quality setting for the font rendering.
    fontStyle: string (from FontStyle);  # Font style (e.g., normal, italic) used for the label text.
    fontVariant: string (from FontVariant);  # Font variant used for the label text.
    fontWeight: string (from FontWeight);  # Font weight (e.g., normal, bold) used for the label text.
    alpha: float;  # Transparency level of the label text.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest");  # Quality level of the label representation.
    material: dict;  # Material properties of the label representation.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict;  # Clipping properties for the label representation.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  # Type of the clipping object.
            invert: any;  # Whether to invert the clipping region.
            position: any;  # Position of the clipping object.
            rotation: any;  # Rotation of the clipping object.
            scale: any;  # Scale of the clipping object.
    instanceGranularity: bool;  # If true, enables granularity at the instance level.
line:
    pointStyle: string (available values are "circle", "square", "fuzzy")  # Style of points used in the line representation.
    multipleBonds: string (available values are "offset", "off", "symmetric")  # How multiple bonds are represented (e.g., offset, off, symmetric).
    includeParent: bool  # Whether to include the parent structure in the representation.
    sizeFactor: float  # Factor by which to scale the size of the lines.
    unitKinds: list (available values are "spheres", "gaussians", "atomic")  # Types of units used in the representation.
    visuals: list (available values are "intra-bond", "inter-bond", "element-point", "element-cross")  # Visual elements to include in the line representation.
    lineSizeAttenuation: bool  # Whether the size of the lines should attenuate with distance.
    ignoreHydrogens: bool  # If true, hydrogen atoms are ignored in the representation.
    ignoreHydrogensVariant: string (available values are "all", "non-polar")  # How hydrogen atoms are ignored (e.g., all, non-polar).
    traceOnly: bool  # If true, only the trace of the structure is used.
    crosses: string (available values are "all", "lone")  # Specifies how crosses are used in the representation (e.g., all, lone).
    crossSize: float  # The size of the crosses in the representation.
    alpha: float  # Transparency level of the line representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest")  # Quality level of the line representation.
    material: dict  # Material properties of the line representation.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict  # Clipping properties for the line representation.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  
            invert: any;  
            position: any;  
            rotation: any;  
            scale: any;
    instanceGranularity: bool  # If true, enables granularity at the instance level.
    pointSizeAttenuation: bool  # Whether the size of points should attenuate with distance.
    includeTypes: list (available values are "covalent", "metal-coordination", "hydrogen-bond", "disulfide", "aromatic", "computed")  # Types of interactions to include in the representation.
    excludeTypes: list (available values are "covalent", "metal-coordination", "hydrogen-bond", "disulfide", "aromatic", "computed")  # Types of interactions to exclude from the representation.
    aromaticBonds: bool  # Whether to specifically render aromatic bonds.
    linkScale: float  # Scaling factor for links in the representation.
    linkSpacing: float  # Spacing between links in the representation.
    aromaticDashCount: float  # Number of dashes used to represent aromatic bonds.
    dashCount: float  # Number of dashes used to represent dashed lines in bonds.
molecular-surface:
    visuals: list (available values are "molecular-surface-mesh", "structure-molecular-surface-mesh", "molecular-surface-wireframe")  # Defines the visual styles to be used in the molecular surface representation.
    bumpFrequency: float  # Controls the frequency of bumps on the surface, affecting its texture.
    sizeFactor: float  # Factor by which to scale the size of the surface.
    ignoreHydrogens: bool  # If true, hydrogen atoms are ignored in the surface calculation.
    ignoreHydrogensVariant: string (available values are "all", "non-polar")  # Specifies how hydrogen atoms are ignored (e.g., all, non-polar).
    traceOnly: bool  # If true, only the trace of the molecular structure is used to generate the surface.
    includeParent: bool  # Whether to include the parent structure in the representation.
    probeRadius: float  # Radius of the probe used to calculate the molecular surface.
    resolution: float  # Controls the resolution of the surface mesh.
    probePositions: float  # Determines the positioning of probes on the surface.
    unitKinds: list (available values are "spheres", "gaussians", "atomic")  # Types of units used in the surface representation.
    lineSizeAttenuation: bool  # Whether the size of lines should attenuate with distance.
    alpha: float  # Transparency level of the surface representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest")  # Quality level of the surface representation.
    material: dict  # Material properties for the molecular surface.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict  # Clipping properties for the molecular surface.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  
            invert: any;  
            position: any;  
            rotation: any;  
            scale: any;
    instanceGranularity: bool  # If true, enables granularity at the instance level.
    smoothColors: dict  # Controls the smoothness of colors on the surface.
        auto: dict;  # Automatically determine color smoothness.
        on: dict;  # Enable smooth colors with customizable resolution and sample stride.
            resolutionFactor: float;  
            sampleStride: float;  
        off: dict;  # Disable color smoothing.
    doubleSided: bool  # If true, the surface will be rendered double-sided.
    flipSided: bool  # If true, the surface normals are flipped, inverting the surface.
    flatShaded: bool  # If true, the surface will be rendered with flat shading.
    ignoreLight: bool  # If true, lighting effects are ignored in the rendering.
    xrayShaded: bool  # If true, the surface is shaded with an X-ray effect.
    transparentBackfaces: string  # Defines how backfaces of the surface are handled when transparent.
    bumpAmplitude: float  # Amplitude of the bumps on the surface, affecting the texture.
orientation:
    visuals: list (available values are "orientation-ellipsoid-mesh")  # Defines the visual style used to represent the orientation, specifically as an ellipsoid mesh.
    bumpFrequency: float  # Controls the frequency of surface bumps, affecting the texture of the orientation ellipsoid.
    sizeFactor: float  # Factor by which to scale the size of the orientation ellipsoid.
    detail: float  # Determines the level of detail in the orientation representation, such as the smoothness of the ellipsoid.
    unitKinds: list (available values are "spheres", "gaussians", "atomic")  # Types of units used in the orientation representation.
    includeParent: bool  # Whether to include the parent structure in the representation.
    doubleSided: bool  # If true, the orientation ellipsoid is rendered double-sided.
    flipSided: bool  # If true, the normals of the orientation ellipsoid are flipped, inverting its surface.
    flatShaded: bool  # If true, the ellipsoid will be rendered with flat shading.
    ignoreLight: bool  # If true, lighting effects are ignored in the rendering of the orientation ellipsoid.
    xrayShaded: bool  # If true, the ellipsoid is shaded with an X-ray effect.
    transparentBackfaces: string  # Defines how backfaces of the orientation ellipsoid are handled when transparent.
    bumpAmplitude: float  # Amplitude of the bumps on the ellipsoid, affecting its texture.
    alpha: float  # Transparency level of the orientation representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest")  # Quality level of the orientation representation.
    material: dict  # Material properties for the orientation ellipsoid.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict  # Clipping properties for the orientation ellipsoid.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  
            invert: any;  
            position: any;  
            rotation: any;  
            scale: any;
    instanceGranularity: bool  # If true, enables granularity at the instance level.
point:
    pointSizeAttenuation: bool  # Controls whether the size of points is attenuated based on their distance from the camera.
    ignoreHydrogens: bool  # If true, hydrogen atoms are ignored in the point representation.
    ignoreHydrogensVariant: string (available values are "all", "non-polar")  # Determines which hydrogen atoms are ignored, either all or only non-polar ones.
    traceOnly: bool  # If true, only the trace of the molecular structure (like backbone atoms) is represented as points.
    unitKinds: list (available values are "spheres", "gaussians", "atomic")  # Types of units used in the point representation.
    includeParent: bool  # Whether to include the parent structure in the point representation.
    sizeFactor: float  # Factor by which to scale the size of the points.
    pointStyle: string (available values are "circle", "square", "fuzzy")  # Style of the points used in the representation, such as circles, squares, or fuzzy points.
    alpha: float  # Transparency level of the point representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest")  # Quality level of the point representation.
    material: dict  # Material properties for the points.
        metalness: float;  # Reflective property of the material, mimicking metal.
        roughness: float;  # Roughness of the material surface.
        bumpiness: float;  # Bumpiness of the material, affecting the texture.
    clip: dict  # Clipping properties for the points.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant used.
        objects: dict;  # Dict of clipping objects with various properties.
            type: any;  
            invert: any;  
            position: any;  
            rotation: any;  
            scale: any;
    instanceGranularity: bool  # If true, enables granularity at the instance level.
spacefill:
    bumpFrequency: float  # Determines the frequency of bump mapping, which affects the surface texture.
    sizeFactor: float  # Scale factor that adjusts the size of the atoms in the spacefill representation.
    detail: float  # Level of detail in the representation, typically affecting how smooth or detailed the surface appears.
    ignoreHydrogens: bool  # If true, hydrogen atoms are excluded from the representation.
    ignoreHydrogensVariant: string (available values are "all", "non-polar")  # Specifies which hydrogen atoms to ignore, either all or just non-polar hydrogens.
    traceOnly: bool  # If true, only the backbone trace of the molecular structure is represented, ignoring side chains and other parts.
    tryUseImpostor: bool  # Determines whether to use impostors for rendering, which can improve performance in some cases.
    unitKinds: list (available values are "spheres", "gaussians", "atomic")  # Defines the types of units used in the spacefill representation.
    includeParent: bool  # Indicates whether the parent structure should be included in the representation.
    doubleSided: bool  # If true, the surface is rendered on both sides, making it visible from inside as well.
    ignoreLight: bool  # If true, lighting effects are ignored, resulting in a flat, unshaded appearance.
    xrayShaded: bool  # If true, the representation will use an X-ray style shading, often used for transparency effects.
    transparentBackfaces: string  # Controls how backfaces (the side of the surface not facing the camera) are rendered when transparency is enabled.
    solidInterior: bool  # If true, the interior of the atoms is rendered as solid rather than hollow.
    bumpAmplitude: float  # Amplitude of bump mapping, which influences the perceived depth of surface textures.
    alpha: float  # Transparency level of the spacefill representation.
    quality: string (available values are "auto", "medium", "high", "low", "custom", "highest", "higher", "lower", "lowest")  # Quality setting for the spacefill representation, affecting rendering detail and performance.
    material: dict  # Material properties for the spacefill representation.
        metalness: float;  # Degree of reflectivity, simulating metallic surfaces.
        roughness: float;  # Surface roughness, affecting how light scatters.
        bumpiness: float;  # Perceived bumpiness or texture of the surface.
    clip: dict  # Clipping properties for the spacefill representation.
        variant: string (available values are "instance", "pixel");  # Type of clipping variant applied.
        objects: dict;  # Dict of clipping objects with specific properties.
            type: any;  
            invert: any;  
            position: any;  
            rotation: any;  
            scale: any;
    instanceGranularity: bool  # Enables granularity at the instance level, which can be useful for distinguishing different parts of the structure.
    flipSided: bool  # If true, flips the rendering of the sides, which can be useful for certain visual effects.
    flatShaded: bool  # If true, renders the surface without smooth shading, resulting in a faceted appearance.
