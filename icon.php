<?php

if (\php_sapi_name() !== 'cli') {
    throw new \RuntimeException('Run in CLI mode only.');
}

if (!\extension_loaded('gd')) {
    throw new \RuntimeException('gd extension must be loaded!');
}

$arguments = $argv;
\array_shift($arguments);

$source = \array_shift($arguments);
$output = \array_shift($arguments);

if ($source === null) {
    throw new \RuntimeException('Must provide source image');
}
if (!\file_exists($source)) {
    throw new \RuntimeException('File not found at: ' . $source);
}

if ($output === null) {
    $output = \dirname($source);
}
if (!\is_dir($output)) {
    \mkdir($output, 0755, true);
}

function resizeImage($source, $size, $output) {
    $imageInfo = \getimagesize($source);
    if (!\is_array($imageInfo)) {
        throw new \InvalidArgumentException('Source must be a image!');
    }
    if ($imageInfo[2] !== IMAGETYPE_PNG) {
        throw new \InvalidArgumentException('Source image must be PNG format!');
    }
    list ($width, $height) = $imageInfo;

    $tempFile = \tempnam('/tmp', '');

    \file_put_contents($tempFile, \file_get_contents($source));

    $image = \imagecreatefrompng($source);
    if ($imageInfo[2] === IMAGETYPE_PNG) {
        \imageinterlace($image, true);
    }

    \imagealphablending($image, true);
    \imagesavealpha($image, true);

    $newImage = \imagecreatetruecolor($size, $size);
    \imagecolorallocate($newImage, 255, 255, 255);
    \imageinterlace($newImage, true);

    \imagecopyresampled(
        $newImage,
        $image,
        0, 0,
        0, 0,
        $size, $size,
        $width,
        $height
    );

    \imagepng($newImage, $output, 9, PNG_ALL_FILTERS);
    \imagedestroy($image);
    \imagedestroy($newImage);

    \unlink($tempFile);
}

function appStoreIcon($source, array &$contents, $size, $scale, $idiom = 'iphone') {
    global $output;

    if ($idiom === 'ios-marketing') {
        $filename = 'iTunesArtwork@1x.png';
    } else {
        $filename = "AppIcon-{$size}x{$size}@{$scale}x.png";
    }
    $outputIcon = $output . DIRECTORY_SEPARATOR . "/AppIcon.appiconset/{$filename}";
    $outputDir = \dirname($outputIcon);
    if (!\is_dir($outputDir)) {
        \mkdir($outputDir, 0755, true);
    }

    $contents['images'][] = [
        'size' => "{$size}x{$size}",
        'idiom' => $idiom,
        'filename' => \basename($outputIcon),
        'scale' => "{$scale}x"
    ];

    resizeImage($source, $size * $scale, $outputIcon);
}

$contentsJson = [
    'images' => [],
    'info' => [
        'version' => 1,
        'author' => 'truonglv'
    ]
];

$appStoreIconSets = [
    'iphone' => [
        'sizes' => [
            20,
            29,
            40,
            60
        ],
        'scales' => [
            2,
            3
        ]
    ],
    'ipad' => [
        'sizes' => [
            20,
            29,
            40,
            76,
            83.5
        ],
        'scales' => [
            1,
            2
        ],
        'scaleVerifyCallback' => function ($size, $scale) {
            if ($size === 83.5 && $scale === 1) {
                return false;
            }

            return true;
        }
    ],
    'ios-marketing' => [
        'sizes' => [
            1024
        ],
        'scales' => [
            1
        ]
    ]
];
$appStoreSizeScaleMap = [];
foreach ($appStoreIconSets as $idiom => $set) {
    foreach ($set['sizes'] as $size) {
        foreach ($set['scales'] as $scale) {
            if (isset($set['scaleVerifyCallback'])) {
                $valid = \call_user_func($set['scaleVerifyCallback'], $size, $scale);
                if ($valid !== true) {
                    echo \sprintf('Skip generate app store image. $idiom=%s $size=%d $scale=%d' . PHP_EOL,
                        $idiom,
                        $size,
                        $scale
                    );

                    continue;
                }
            }

            echo \sprintf('Generate app store image. $idiom=%s $size=%d $scale=%d' . PHP_EOL,
                $idiom,
                $size,
                $scale
            );

            appStoreIcon($source, $contentsJson, $size, $scale, $idiom);
        }
    }
}

\file_put_contents(
    $output . DIRECTORY_SEPARATOR . '/AppIcon.appiconset/Contents.json',
    \json_encode($contentsJson, JSON_PRETTY_PRINT)
);

// Generate android play store icons
$androidIconSets = [
    'mipmap-hdpi' => 72,
    'mipmap-mdpi' => 48,
    'mipmap-xhdpi' => 96,
    'mipmap-xxhdpi' => 144,
    'mipmap-xxxhdpi' => 192
];

$androidOutput = $output . DIRECTORY_SEPARATOR . 'android';
foreach ($androidIconSets as $sizeName => $size) {
    $androidOutputFile = $androidOutput . DIRECTORY_SEPARATOR . $sizeName . DIRECTORY_SEPARATOR . 'ic_launcher.png';
    $androidOutputFileDir = \dirname($androidOutputFile);
    if (!\is_dir($androidOutputFileDir)) {
        \mkdir($androidOutputFileDir, 0755, true);
    }

    echo \sprintf('Generate android app icon $sizeName=%s $size=%d $output=%s' . PHP_EOL,
        $sizeName,
        $size,
        $androidOutputFile
    );

    resizeImage(
        $source,
        $size,
        $androidOutputFile
    );
}

echo 'All icons generated!' . PHP_EOL;
echo 'Output directory: ' . $output . PHP_EOL;

exit(0);