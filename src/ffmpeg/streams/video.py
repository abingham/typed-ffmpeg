from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..base import FilterableStream, FilterNode
from ..schema import DefaultFloat, DefaultInt, DefaultStr, StreamType

if TYPE_CHECKING:
    from .audio import AudioStream


class VideoStream(FilterableStream):
    @property
    def video(self) -> "VideoStream":
        return VideoStream(node=self.node, index=self.index, selector=StreamType.video)

    @property
    def audio(self) -> "AudioStream":
        raise NotImplementedError("Cannot convert video to audio")

    def addroi(
        self,
        *,
        x: str | DefaultStr = DefaultStr("0"),
        y: str | DefaultStr = DefaultStr("0"),
        w: str | DefaultStr = DefaultStr("0"),
        h: str | DefaultStr = DefaultStr("0"),
        qoffset: float | DefaultFloat = DefaultFloat(-0.1),
        clear: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.1 addroi
        Mark a region of interest in a video frame.

        The frame data is passed through unchanged, but metadata is attached
        to the frame indicating regions of interest which can affect the
        behaviour of later encoding.  Multiple regions can be marked by
        applying the filter multiple times.

        Parameters:
        ----------

        :param str x: Region distance in pixels from the left edge of the frame.
        :param str y: Region distance in pixels from the top edge of the frame.
        :param str w: Region width in pixels.
        :param str h: Region height in pixels. The parameters x, y, w and h are expressions, and may contain the following variables: iw Width of the input frame. ih Height of the input frame.
        :param float qoffset: Quantisation offset to apply within the region. This must be a real value in the range -1 to +1. A value of zero indicates no quality change. A negative value asks for better quality (less quantisation), while a positive value asks for worse quality (greater quantisation). The range is calibrated so that the extreme values indicate the largest possible offset - if the rest of the frame is encoded with the worst possible quality, an offset of -1 indicates that this region should be encoded with the best possible quality anyway. Intermediate values are then interpolated in some codec-dependent way. For example, in 10-bit H.264 the quantisation parameter varies between -12 and 51. A typical qoffset value of -1/10 therefore indicates that this region should be encoded with a QP around one-tenth of the full range better than the rest of the frame. So, if most of the frame were to be encoded with a QP of around 30, this region would get a QP of around 24 (an offset of approximately -1/10 * (51 - -12) = -6.3). An extreme value of -1 would indicate that this region should be encoded with the best possible quality regardless of the treatment of the rest of the frame - that is, should be encoded at a QP of -12.
        :param bool clear: If set to true, remove any existing regions of interest marked on the frame before adding the new one.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#addroi

        """
        filter_node = FilterNode(
            name="addroi",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "qoffset": qoffset,
                "clear": clear,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def alphaextract(self, **kwargs: Any) -> "VideoStream":
        """

        11.2 alphaextract
        Extract the alpha component from the input as a grayscale video. This
        is especially useful with the alphamerge filter.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#alphaextract

        """
        filter_node = FilterNode(
            name="alphaextract",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def alphamerge(self, _alpha: "VideoStream", **kwargs: Any) -> "VideoStream":
        """

        11.3 alphamerge
        Add or replace the alpha component of the primary input with the
        grayscale value of a second input. This is intended for use with
        alphaextract to allow the transmission or storage of frame
        sequences that have alpha in a format that doesn’t support an alpha
        channel.

        For example, to reconstruct full frames from a normal YUV-encoded video
        and a separate video created with alphaextract, you might use:

        movie=in_alpha.mkv [alpha]; [in][alpha] alphamerge [out]

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#alphamerge

        """
        filter_node = FilterNode(
            name="alphamerge",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _alpha,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def amplify(
        self,
        *,
        radius: int | DefaultInt = DefaultInt(2),
        factor: float | DefaultFloat = DefaultFloat(2.0),
        threshold: float | DefaultFloat = DefaultFloat(10.0),
        tolerance: float | DefaultFloat = DefaultFloat(0.0),
        low: float | DefaultFloat = DefaultFloat(65535.0),
        high: float | DefaultFloat = DefaultFloat(65535.0),
        planes: str | DefaultStr = DefaultStr(7),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.4 amplify
        Amplify differences between current pixel and pixels of adjacent frames in
        same pixel location.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int radius: Set frame radius. Default is 2. Allowed range is from 1 to 63. For example radius of 3 will instruct filter to calculate average of 7 frames.
        :param float factor: Set factor to amplify difference. Default is 2. Allowed range is from 0 to 65535.
        :param float threshold: Set threshold for difference amplification. Any difference greater or equal to this value will not alter source pixel. Default is 10. Allowed range is from 0 to 65535.
        :param float tolerance: Set tolerance for difference amplification. Any difference lower to this value will not alter source pixel. Default is 0. Allowed range is from 0 to 65535.
        :param float low: Set lower limit for changing source pixel. Default is 65535. Allowed range is from 0 to 65535. This option controls maximum possible value that will decrease source pixel value.
        :param float high: Set high limit for changing source pixel. Default is 65535. Allowed range is from 0 to 65535. This option controls maximum possible value that will increase source pixel value.
        :param str planes: Set which planes to filter. Default is all. Allowed range is from 0 to 15.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#amplify

        """
        filter_node = FilterNode(
            name="amplify",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "radius": radius,
                "factor": factor,
                "threshold": threshold,
                "tolerance": tolerance,
                "low": low,
                "high": high,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def ass(
        self,
        *,
        filename: str,
        original_size: str,
        fontsdir: str,
        alpha: bool | DefaultInt = DefaultInt(0),
        shaping: int | Literal["auto", "simple", "complex"] | DefaultStr = DefaultStr("auto"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.5 ass
        Same as the subtitles filter, except that it doesn’t require libavcodec
        and libavformat to work. On the other hand, it is limited to ASS (Advanced
        Substation Alpha) subtitles files.

        This filter accepts the following option in addition to the common options from
        the subtitles filter:

        Parameters:
        ----------

        :param str filename: None
        :param str original_size: None
        :param str fontsdir: None
        :param bool alpha: None
        :param int shaping: Set the shaping engine Available values are: ‘auto’ The default libass shaping engine, which is the best available. ‘simple’ Fast, font-agnostic shaper that can do only substitutions ‘complex’ Slower shaper using OpenType for substitutions and positioning The default is auto.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#ass

        """
        filter_node = FilterNode(
            name="ass",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "filename": filename,
                "original_size": original_size,
                "fontsdir": fontsdir,
                "alpha": alpha,
                "shaping": shaping,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def atadenoise(
        self,
        *,
        _0a: float | DefaultFloat = DefaultFloat(0.02),
        _0b: float | DefaultFloat = DefaultFloat(0.04),
        _1a: float | DefaultFloat = DefaultFloat(0.02),
        _1b: float | DefaultFloat = DefaultFloat(0.04),
        _2a: float | DefaultFloat = DefaultFloat(0.02),
        _2b: float | DefaultFloat = DefaultFloat(0.04),
        s: int | DefaultInt = DefaultInt(9),
        p: str | DefaultStr = DefaultStr(7),
        a: int | Literal["p", "s"] | DefaultStr = DefaultStr("p"),
        _0s: float | DefaultFloat = DefaultFloat(32767.0),
        _1s: float | DefaultFloat = DefaultFloat(32767.0),
        _2s: float | DefaultFloat = DefaultFloat(32767.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.6 atadenoise
        Apply an Adaptive Temporal Averaging Denoiser to the video input.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float _0a: Set threshold A for 1st plane. Default is 0.02. Valid range is 0 to 0.3.
        :param float _0b: Set threshold B for 1st plane. Default is 0.04. Valid range is 0 to 5.
        :param float _1a: Set threshold A for 2nd plane. Default is 0.02. Valid range is 0 to 0.3.
        :param float _1b: Set threshold B for 2nd plane. Default is 0.04. Valid range is 0 to 5.
        :param float _2a: Set threshold A for 3rd plane. Default is 0.02. Valid range is 0 to 0.3.
        :param float _2b: Set threshold B for 3rd plane. Default is 0.04. Valid range is 0 to 5. Threshold A is designed to react on abrupt changes in the input signal and threshold B is designed to react on continuous changes in the input signal.
        :param int s: Set number of frames filter will use for averaging. Default is 9. Must be odd number in range [5, 129].
        :param str p: Set what planes of frame filter will use for averaging. Default is all.
        :param int a: Set what variant of algorithm filter will use for averaging. Default is p parallel. Alternatively can be set to s serial. Parallel can be faster then serial, while other way around is never true. Parallel will abort early on first change being greater then thresholds, while serial will continue processing other side of frames if they are equal or below thresholds.
        :param float _0s: Set sigma for 1st plane, 2nd plane or 3rd plane. Default is 32767. Valid range is from 0 to 32767. This options controls weight for each pixel in radius defined by size. Default value means every pixel have same weight. Setting this option to 0 effectively disables filtering.
        :param float _1s: Set sigma for 1st plane, 2nd plane or 3rd plane. Default is 32767. Valid range is from 0 to 32767. This options controls weight for each pixel in radius defined by size. Default value means every pixel have same weight. Setting this option to 0 effectively disables filtering.
        :param float _2s: Set sigma for 1st plane, 2nd plane or 3rd plane. Default is 32767. Valid range is from 0 to 32767. This options controls weight for each pixel in radius defined by size. Default value means every pixel have same weight. Setting this option to 0 effectively disables filtering.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#atadenoise

        """
        filter_node = FilterNode(
            name="atadenoise",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "0a": _0a,
                "0b": _0b,
                "1a": _1a,
                "1b": _1b,
                "2a": _2a,
                "2b": _2b,
                "s": s,
                "p": p,
                "a": a,
                "0s": _0s,
                "1s": _1s,
                "2s": _2s,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def avgblur(
        self,
        *,
        sizeX: int | DefaultInt = DefaultInt(1),
        planes: int | DefaultStr = DefaultStr("0xF"),
        sizeY: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.7 avgblur
        Apply average blur filter.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int sizeX: Set horizontal radius size.
        :param int planes: Set which planes to filter. By default all planes are filtered.
        :param int sizeY: Set vertical radius size, if zero it will be same as sizeX. Default is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#avgblur

        """
        filter_node = FilterNode(
            name="avgblur",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "sizeX": sizeX,
                "planes": planes,
                "sizeY": sizeY,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def avgblur_opencl(
        self,
        *,
        sizeX: int | DefaultInt = DefaultInt(1),
        planes: int | DefaultStr = DefaultStr("0xF"),
        sizeY: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.1 avgblur_opencl
        Apply average blur filter.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int sizeX: Set horizontal radius size. Range is [1, 1024] and default value is 1.
        :param int planes: Set which planes to filter. Default value is 0xf, by which all planes are processed.
        :param int sizeY: Set vertical radius size. Range is [1, 1024] and default value is 0. If zero, sizeX value will be used.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#avgblur_005fopencl

        """
        filter_node = FilterNode(
            name="avgblur_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "sizeX": sizeX,
                "planes": planes,
                "sizeY": sizeY,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def avgblur_vulkan(
        self,
        *,
        sizeX: int | DefaultInt = DefaultInt(3),
        sizeY: int | DefaultInt = DefaultInt(3),
        planes: int | DefaultStr = DefaultStr("0xF"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        14.1 avgblur_vulkan
        Apply an average blur filter, implemented on the GPU using Vulkan.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int sizeX: Set horizontal radius size. Range is [1, 32] and default value is 3.
        :param int sizeY: Set vertical radius size. Range is [1, 32] and default value is 3.
        :param int planes: Set which planes to filter. Default value is 0xf, by which all planes are processed.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#avgblur_005fvulkan

        """
        filter_node = FilterNode(
            name="avgblur_vulkan",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "sizeX": sizeX,
                "sizeY": sizeY,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def backgroundkey(
        self,
        *,
        threshold: float | DefaultFloat = DefaultFloat(0.08),
        similarity: float | DefaultFloat = DefaultFloat(0.1),
        blend: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.8 backgroundkey
        Turns a static background into transparency.

        The filter accepts the following option:

        Parameters:
        ----------

        :param float threshold: Threshold for scene change detection.
        :param float similarity: Similarity percentage with the background.
        :param float blend: Set the blend amount for pixels that are not similar.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#backgroundkey

        """
        filter_node = FilterNode(
            name="backgroundkey",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "threshold": threshold,
                "similarity": similarity,
                "blend": blend,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def bbox(self, *, min_val: int | DefaultInt = DefaultInt(16), **kwargs: Any) -> "VideoStream":
        """

        11.9 bbox
        Compute the bounding box for the non-black pixels in the input frame
        luma plane.

        This filter computes the bounding box containing all the pixels with a
        luma value greater than the minimum allowed value.
        The parameters describing the bounding box are printed on the filter
        log.

        The filter accepts the following option:

        Parameters:
        ----------

        :param int min_val: Set the minimal luma value. Default is 16.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#bbox

        """
        filter_node = FilterNode(
            name="bbox",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "min_val": min_val,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def bench(
        self, *, action: int | Literal["start", "stop"] | DefaultStr = DefaultStr("start"), **kwargs: Any
    ) -> "VideoStream":
        """

        18.8 bench, abench
        Benchmark part of a filtergraph.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int action: Start or stop a timer. Available values are: ‘start’ Get the current time, set it as frame metadata (using the key lavfi.bench.start_time), and forward the frame to the next filter. ‘stop’ Get the current time and fetch the lavfi.bench.start_time metadata from the input frame metadata to get the time difference. Time difference, average, maximum and minimum time (respectively t, avg, max and min) are then printed. The timestamps are expressed in seconds.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#bench_002c-abench

        """
        filter_node = FilterNode(
            name="bench",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "action": action,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def bilateral(
        self,
        *,
        sigmaS: float | DefaultFloat = DefaultFloat(0.1),
        sigmaR: float | DefaultFloat = DefaultFloat(0.1),
        planes: int | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.10 bilateral
        Apply bilateral filter, spatial smoothing while preserving edges.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float sigmaS: Set sigma of gaussian function to calculate spatial weight. Allowed range is 0 to 512. Default is 0.1.
        :param float sigmaR: Set sigma of gaussian function to calculate range weight. Allowed range is 0 to 1. Default is 0.1.
        :param int planes: Set planes to filter. Default is first only.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#bilateral

        """
        filter_node = FilterNode(
            name="bilateral",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "sigmaS": sigmaS,
                "sigmaR": sigmaR,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def bilateral_cuda(
        self,
        *,
        sigmaS: float | DefaultFloat = DefaultFloat(0.1),
        sigmaR: float | DefaultFloat = DefaultFloat(0.1),
        window_size: int | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.11 bilateral_cuda
        CUDA accelerated bilateral filter, an edge preserving filter.
        This filter is mathematically accurate thanks to the use of GPU acceleration.
        For best output quality, use one to one chroma subsampling, i.e. yuv444p format.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float sigmaS: Set sigma of gaussian function to calculate spatial weight, also called sigma space. Allowed range is 0.1 to 512. Default is 0.1.
        :param float sigmaR: Set sigma of gaussian function to calculate color range weight, also called sigma color. Allowed range is 0.1 to 512. Default is 0.1.
        :param int window_size: Set window size of the bilateral function to determine the number of neighbours to loop on. If the number entered is even, one will be added automatically. Allowed range is 1 to 255. Default is 1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#bilateral_005fcuda

        """
        filter_node = FilterNode(
            name="bilateral_cuda",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "sigmaS": sigmaS,
                "sigmaR": sigmaR,
                "window_size": window_size,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def bitplanenoise(
        self, *, bitplane: int | DefaultInt = DefaultInt(1), filter: bool | DefaultInt = DefaultInt(0), **kwargs: Any
    ) -> "VideoStream":
        """

        11.12 bitplanenoise
        Show and measure bit plane noise.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int bitplane: Set which plane to analyze. Default is 1.
        :param bool filter: Filter out noisy pixels from bitplane set above. Default is disabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#bitplanenoise

        """
        filter_node = FilterNode(
            name="bitplanenoise",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "bitplane": bitplane,
                "filter": filter,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def blackdetect(
        self,
        *,
        d: float | DefaultFloat = DefaultFloat(2.0),
        picture_black_ratio_th: float | DefaultFloat = DefaultFloat(0.98),
        pixel_black_th: float | DefaultFloat = DefaultFloat(0.1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.13 blackdetect
        Detect video intervals that are (almost) completely black. Can be
        useful to detect chapter transitions, commercials, or invalid
        recordings.

        The filter outputs its detection analysis to both the log as well as
        frame metadata. If a black segment of at least the specified minimum
        duration is found, a line with the start and end timestamps as well
        as duration is printed to the log with level info. In addition,
        a log line with level debug is printed per frame showing the
        black amount detected for that frame.

        The filter also attaches metadata to the first frame of a black
        segment with key lavfi.black_start and to the first frame
        after the black segment ends with key lavfi.black_end. The
        value is the frame’s timestamp. This metadata is added regardless
        of the minimum duration specified.

        The filter accepts the following options:


        The following example sets the maximum pixel threshold to the minimum
        value, and detects only black intervals of 2 or more seconds:

        blackdetect=d=2:pix_th=0.00

        Parameters:
        ----------

        :param float d: Set the minimum detected black duration expressed in seconds. It must be a non-negative floating point number. Default value is 2.0.
        :param float picture_black_ratio_th: Set the threshold for considering a picture "black". Express the minimum value for the ratio: nb_black_pixels / nb_pixels for which a picture is considered black. Default value is 0.98.
        :param float pixel_black_th: Set the threshold for considering a pixel "black". The threshold expresses the maximum pixel luma value for which a pixel is considered "black". The provided value is scaled according to the following equation: absolute_threshold = luma_minimum_value + pixel_black_th * luma_range_size luma_range_size and luma_minimum_value depend on the input video format, the range is [0-255] for YUV full-range formats and [16-235] for YUV non full-range formats. Default value is 0.10.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#blackdetect

        """
        filter_node = FilterNode(
            name="blackdetect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "d": d,
                "picture_black_ratio_th": picture_black_ratio_th,
                "pixel_black_th": pixel_black_th,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def blackframe(
        self, *, amount: int | DefaultInt = DefaultInt(98), threshold: int | DefaultInt = DefaultInt(32), **kwargs: Any
    ) -> "VideoStream":
        """

        11.14 blackframe
        Detect frames that are (almost) completely black. Can be useful to
        detect chapter transitions or commercials. Output lines consist of
        the frame number of the detected frame, the percentage of blackness,
        the position in the file if known or -1 and the timestamp in seconds.

        In order to display the output lines, you need to set the loglevel at
        least to the AV_LOG_INFO value.

        This filter exports frame metadata lavfi.blackframe.pblack.
        The value represents the percentage of pixels in the picture that
        are below the threshold value.

        It accepts the following parameters:

        Parameters:
        ----------

        :param int amount: The percentage of the pixels that have to be below the threshold; it defaults to 98.
        :param int threshold: The threshold below which a pixel value is considered black; it defaults to 32.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#blackframe

        """
        filter_node = FilterNode(
            name="blackframe",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "amount": amount,
                "threshold": threshold,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def blend(
        self,
        _bottom: "VideoStream",
        *,
        c0_mode: int
        | Literal[
            "addition",
            "addition128",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "difference128",
            "grainextract",
            "divide",
            "dodge",
            "exclusion",
            "extremity",
            "freeze",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor",
            "softdifference",
            "geometric",
            "harmonic",
            "bleach",
            "stain",
            "interpolate",
            "hardoverlay",
        ]
        | DefaultStr = DefaultStr(0),
        c1_mode: int
        | Literal[
            "addition",
            "addition128",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "difference128",
            "grainextract",
            "divide",
            "dodge",
            "exclusion",
            "extremity",
            "freeze",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor",
            "softdifference",
            "geometric",
            "harmonic",
            "bleach",
            "stain",
            "interpolate",
            "hardoverlay",
        ]
        | DefaultStr = DefaultStr(0),
        c2_mode: int
        | Literal[
            "addition",
            "addition128",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "difference128",
            "grainextract",
            "divide",
            "dodge",
            "exclusion",
            "extremity",
            "freeze",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor",
            "softdifference",
            "geometric",
            "harmonic",
            "bleach",
            "stain",
            "interpolate",
            "hardoverlay",
        ]
        | DefaultStr = DefaultStr(0),
        c3_mode: int
        | Literal[
            "addition",
            "addition128",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "difference128",
            "grainextract",
            "divide",
            "dodge",
            "exclusion",
            "extremity",
            "freeze",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor",
            "softdifference",
            "geometric",
            "harmonic",
            "bleach",
            "stain",
            "interpolate",
            "hardoverlay",
        ]
        | DefaultStr = DefaultStr(0),
        all_mode: int
        | Literal[
            "addition",
            "addition128",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "difference128",
            "grainextract",
            "divide",
            "dodge",
            "exclusion",
            "extremity",
            "freeze",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor",
            "softdifference",
            "geometric",
            "harmonic",
            "bleach",
            "stain",
            "interpolate",
            "hardoverlay",
        ]
        | DefaultStr = DefaultStr(-1),
        c0_expr: str,
        c1_expr: str,
        c2_expr: str,
        c3_expr: str,
        all_expr: str,
        c0_opacity: float | DefaultFloat = DefaultFloat(1.0),
        c1_opacity: float | DefaultFloat = DefaultFloat(1.0),
        c2_opacity: float | DefaultFloat = DefaultFloat(1.0),
        c3_opacity: float | DefaultFloat = DefaultFloat(1.0),
        all_opacity: float | DefaultFloat = DefaultFloat(1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.15 blend
        Blend two video frames into each other.

        The blend filter takes two input streams and outputs one
        stream, the first input is the "top" layer and second input is
        "bottom" layer.  By default, the output terminates when the longest input terminates.

        The tblend (time blend) filter takes two consecutive frames
        from one single stream, and outputs the result obtained by blending
        the new frame on top of the old frame.

        A description of the accepted options follows.


        The blend filter also supports the framesync options.

        Parameters:
        ----------

        :param int c0_mode: Set blend mode for specific pixel component or all pixel components in case of all_mode. Default value is normal. Available values for component modes are: ‘addition’ ‘and’ ‘average’ ‘bleach’ ‘burn’ ‘darken’ ‘difference’ ‘divide’ ‘dodge’ ‘exclusion’ ‘extremity’ ‘freeze’ ‘geometric’ ‘glow’ ‘grainextract’ ‘grainmerge’ ‘hardlight’ ‘hardmix’ ‘hardoverlay’ ‘harmonic’ ‘heat’ ‘interpolate’ ‘lighten’ ‘linearlight’ ‘multiply’ ‘multiply128’ ‘negation’ ‘normal’ ‘or’ ‘overlay’ ‘phoenix’ ‘pinlight’ ‘reflect’ ‘screen’ ‘softdifference’ ‘softlight’ ‘stain’ ‘subtract’ ‘vividlight’ ‘xor’
        :param int c1_mode: Set blend mode for specific pixel component or all pixel components in case of all_mode. Default value is normal. Available values for component modes are: ‘addition’ ‘and’ ‘average’ ‘bleach’ ‘burn’ ‘darken’ ‘difference’ ‘divide’ ‘dodge’ ‘exclusion’ ‘extremity’ ‘freeze’ ‘geometric’ ‘glow’ ‘grainextract’ ‘grainmerge’ ‘hardlight’ ‘hardmix’ ‘hardoverlay’ ‘harmonic’ ‘heat’ ‘interpolate’ ‘lighten’ ‘linearlight’ ‘multiply’ ‘multiply128’ ‘negation’ ‘normal’ ‘or’ ‘overlay’ ‘phoenix’ ‘pinlight’ ‘reflect’ ‘screen’ ‘softdifference’ ‘softlight’ ‘stain’ ‘subtract’ ‘vividlight’ ‘xor’
        :param int c2_mode: Set blend mode for specific pixel component or all pixel components in case of all_mode. Default value is normal. Available values for component modes are: ‘addition’ ‘and’ ‘average’ ‘bleach’ ‘burn’ ‘darken’ ‘difference’ ‘divide’ ‘dodge’ ‘exclusion’ ‘extremity’ ‘freeze’ ‘geometric’ ‘glow’ ‘grainextract’ ‘grainmerge’ ‘hardlight’ ‘hardmix’ ‘hardoverlay’ ‘harmonic’ ‘heat’ ‘interpolate’ ‘lighten’ ‘linearlight’ ‘multiply’ ‘multiply128’ ‘negation’ ‘normal’ ‘or’ ‘overlay’ ‘phoenix’ ‘pinlight’ ‘reflect’ ‘screen’ ‘softdifference’ ‘softlight’ ‘stain’ ‘subtract’ ‘vividlight’ ‘xor’
        :param int c3_mode: Set blend mode for specific pixel component or all pixel components in case of all_mode. Default value is normal. Available values for component modes are: ‘addition’ ‘and’ ‘average’ ‘bleach’ ‘burn’ ‘darken’ ‘difference’ ‘divide’ ‘dodge’ ‘exclusion’ ‘extremity’ ‘freeze’ ‘geometric’ ‘glow’ ‘grainextract’ ‘grainmerge’ ‘hardlight’ ‘hardmix’ ‘hardoverlay’ ‘harmonic’ ‘heat’ ‘interpolate’ ‘lighten’ ‘linearlight’ ‘multiply’ ‘multiply128’ ‘negation’ ‘normal’ ‘or’ ‘overlay’ ‘phoenix’ ‘pinlight’ ‘reflect’ ‘screen’ ‘softdifference’ ‘softlight’ ‘stain’ ‘subtract’ ‘vividlight’ ‘xor’
        :param int all_mode: Set blend mode for specific pixel component or all pixel components in case of all_mode. Default value is normal. Available values for component modes are: ‘addition’ ‘and’ ‘average’ ‘bleach’ ‘burn’ ‘darken’ ‘difference’ ‘divide’ ‘dodge’ ‘exclusion’ ‘extremity’ ‘freeze’ ‘geometric’ ‘glow’ ‘grainextract’ ‘grainmerge’ ‘hardlight’ ‘hardmix’ ‘hardoverlay’ ‘harmonic’ ‘heat’ ‘interpolate’ ‘lighten’ ‘linearlight’ ‘multiply’ ‘multiply128’ ‘negation’ ‘normal’ ‘or’ ‘overlay’ ‘phoenix’ ‘pinlight’ ‘reflect’ ‘screen’ ‘softdifference’ ‘softlight’ ‘stain’ ‘subtract’ ‘vividlight’ ‘xor’
        :param str c0_expr: Set blend expression for specific pixel component or all pixel components in case of all_expr. Note that related mode options will be ignored if those are set. The expressions can use the following variables: N The sequential number of the filtered frame, starting from 0. X Y the coordinates of the current sample W H the width and height of currently filtered plane SW SH Width and height scale for the plane being filtered. It is the ratio between the dimensions of the current plane to the luma plane, e.g. for a yuv420p frame, the values are 1,1 for the luma plane and 0.5,0.5 for the chroma planes. T Time of the current frame, expressed in seconds. TOP, A Value of pixel component at current location for first video frame (top layer). BOTTOM, B Value of pixel component at current location for second video frame (bottom layer).
        :param str c1_expr: Set blend expression for specific pixel component or all pixel components in case of all_expr. Note that related mode options will be ignored if those are set. The expressions can use the following variables: N The sequential number of the filtered frame, starting from 0. X Y the coordinates of the current sample W H the width and height of currently filtered plane SW SH Width and height scale for the plane being filtered. It is the ratio between the dimensions of the current plane to the luma plane, e.g. for a yuv420p frame, the values are 1,1 for the luma plane and 0.5,0.5 for the chroma planes. T Time of the current frame, expressed in seconds. TOP, A Value of pixel component at current location for first video frame (top layer). BOTTOM, B Value of pixel component at current location for second video frame (bottom layer).
        :param str c2_expr: Set blend expression for specific pixel component or all pixel components in case of all_expr. Note that related mode options will be ignored if those are set. The expressions can use the following variables: N The sequential number of the filtered frame, starting from 0. X Y the coordinates of the current sample W H the width and height of currently filtered plane SW SH Width and height scale for the plane being filtered. It is the ratio between the dimensions of the current plane to the luma plane, e.g. for a yuv420p frame, the values are 1,1 for the luma plane and 0.5,0.5 for the chroma planes. T Time of the current frame, expressed in seconds. TOP, A Value of pixel component at current location for first video frame (top layer). BOTTOM, B Value of pixel component at current location for second video frame (bottom layer).
        :param str c3_expr: Set blend expression for specific pixel component or all pixel components in case of all_expr. Note that related mode options will be ignored if those are set. The expressions can use the following variables: N The sequential number of the filtered frame, starting from 0. X Y the coordinates of the current sample W H the width and height of currently filtered plane SW SH Width and height scale for the plane being filtered. It is the ratio between the dimensions of the current plane to the luma plane, e.g. for a yuv420p frame, the values are 1,1 for the luma plane and 0.5,0.5 for the chroma planes. T Time of the current frame, expressed in seconds. TOP, A Value of pixel component at current location for first video frame (top layer). BOTTOM, B Value of pixel component at current location for second video frame (bottom layer).
        :param str all_expr: Set blend expression for specific pixel component or all pixel components in case of all_expr. Note that related mode options will be ignored if those are set. The expressions can use the following variables: N The sequential number of the filtered frame, starting from 0. X Y the coordinates of the current sample W H the width and height of currently filtered plane SW SH Width and height scale for the plane being filtered. It is the ratio between the dimensions of the current plane to the luma plane, e.g. for a yuv420p frame, the values are 1,1 for the luma plane and 0.5,0.5 for the chroma planes. T Time of the current frame, expressed in seconds. TOP, A Value of pixel component at current location for first video frame (top layer). BOTTOM, B Value of pixel component at current location for second video frame (bottom layer).
        :param float c0_opacity: Set blend opacity for specific pixel component or all pixel components in case of all_opacity. Only used in combination with pixel component blend modes.
        :param float c1_opacity: Set blend opacity for specific pixel component or all pixel components in case of all_opacity. Only used in combination with pixel component blend modes.
        :param float c2_opacity: Set blend opacity for specific pixel component or all pixel components in case of all_opacity. Only used in combination with pixel component blend modes.
        :param float c3_opacity: Set blend opacity for specific pixel component or all pixel components in case of all_opacity. Only used in combination with pixel component blend modes.
        :param float all_opacity: Set blend opacity for specific pixel component or all pixel components in case of all_opacity. Only used in combination with pixel component blend modes.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#blend

        """
        filter_node = FilterNode(
            name="blend",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _bottom,
            ],
            kwargs={
                "c0_mode": c0_mode,
                "c1_mode": c1_mode,
                "c2_mode": c2_mode,
                "c3_mode": c3_mode,
                "all_mode": all_mode,
                "c0_expr": c0_expr,
                "c1_expr": c1_expr,
                "c2_expr": c2_expr,
                "c3_expr": c3_expr,
                "all_expr": all_expr,
                "c0_opacity": c0_opacity,
                "c1_opacity": c1_opacity,
                "c2_opacity": c2_opacity,
                "c3_opacity": c3_opacity,
                "all_opacity": all_opacity,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def blend_vulkan(
        self,
        _bottom: "VideoStream",
        *,
        c0_mode: int | Literal["normal", "multiply"] | DefaultStr = DefaultStr(0),
        c1_mode: int | Literal["normal", "multiply"] | DefaultStr = DefaultStr(0),
        c2_mode: int | Literal["normal", "multiply"] | DefaultStr = DefaultStr(0),
        c3_mode: int | Literal["normal", "multiply"] | DefaultStr = DefaultStr(0),
        all_mode: int | Literal["normal", "multiply"] | DefaultStr = DefaultStr(-1),
        c0_opacity: float | DefaultFloat = DefaultFloat(1.0),
        c1_opacity: float | DefaultFloat = DefaultFloat(1.0),
        c2_opacity: float | DefaultFloat = DefaultFloat(1.0),
        c3_opacity: float | DefaultFloat = DefaultFloat(1.0),
        all_opacity: float | DefaultFloat = DefaultFloat(1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        14.2 blend_vulkan
        Blend two Vulkan frames into each other.

        The blend filter takes two input streams and outputs one
        stream, the first input is the "top" layer and second input is
        "bottom" layer.  By default, the output terminates when the longest input terminates.

        A description of the accepted options follows.

        Parameters:
        ----------

        :param int c0_mode: Set blend mode for specific pixel component or all pixel components in case of all_mode. Default value is normal. Available values for component modes are: ‘normal’ ‘multiply’
        :param int c1_mode: Set blend mode for specific pixel component or all pixel components in case of all_mode. Default value is normal. Available values for component modes are: ‘normal’ ‘multiply’
        :param int c2_mode: Set blend mode for specific pixel component or all pixel components in case of all_mode. Default value is normal. Available values for component modes are: ‘normal’ ‘multiply’
        :param int c3_mode: Set blend mode for specific pixel component or all pixel components in case of all_mode. Default value is normal. Available values for component modes are: ‘normal’ ‘multiply’
        :param int all_mode: Set blend mode for specific pixel component or all pixel components in case of all_mode. Default value is normal. Available values for component modes are: ‘normal’ ‘multiply’
        :param float c0_opacity: None
        :param float c1_opacity: None
        :param float c2_opacity: None
        :param float c3_opacity: None
        :param float all_opacity: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#blend_005fvulkan

        """
        filter_node = FilterNode(
            name="blend_vulkan",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _bottom,
            ],
            kwargs={
                "c0_mode": c0_mode,
                "c1_mode": c1_mode,
                "c2_mode": c2_mode,
                "c3_mode": c3_mode,
                "all_mode": all_mode,
                "c0_opacity": c0_opacity,
                "c1_opacity": c1_opacity,
                "c2_opacity": c2_opacity,
                "c3_opacity": c3_opacity,
                "all_opacity": all_opacity,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def blockdetect(
        self,
        *,
        period_min: int | DefaultInt = DefaultInt(3),
        period_max: int | DefaultInt = DefaultInt(24),
        planes: int | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.16 blockdetect
        Determines blockiness of frames without altering the input frames.

        Based on Remco Muijs and Ihor Kirenko: "A no-reference blocking artifact measure for adaptive video processing." 2005 13th European signal processing conference.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int period_min: Set minimum and maximum values for determining pixel grids (periods). Default values are [3,24].
        :param int period_max: Set minimum and maximum values for determining pixel grids (periods). Default values are [3,24].
        :param int planes: Set planes to filter. Default is first only.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#blockdetect

        """
        filter_node = FilterNode(
            name="blockdetect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "period_min": period_min,
                "period_max": period_max,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def blurdetect(
        self,
        *,
        high: float | DefaultStr = DefaultStr("30/255."),
        low: float | DefaultStr = DefaultStr("15/255."),
        radius: int | DefaultInt = DefaultInt(50),
        block_pct: int | DefaultInt = DefaultInt(80),
        block_width: int | DefaultInt = DefaultInt(-1),
        block_height: int | DefaultInt = DefaultInt(-1),
        planes: int | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.17 blurdetect
        Determines blurriness of frames without altering the input frames.

        Based on Marziliano, Pina, et al. "A no-reference perceptual blur metric."
        Allows for a block-based abbreviation.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float high: Set low and high threshold values used by the Canny thresholding algorithm. The high threshold selects the "strong" edge pixels, which are then connected through 8-connectivity with the "weak" edge pixels selected by the low threshold. low and high threshold values must be chosen in the range [0,1], and low should be lesser or equal to high. Default value for low is 20/255, and default value for high is 50/255.
        :param float low: Set low and high threshold values used by the Canny thresholding algorithm. The high threshold selects the "strong" edge pixels, which are then connected through 8-connectivity with the "weak" edge pixels selected by the low threshold. low and high threshold values must be chosen in the range [0,1], and low should be lesser or equal to high. Default value for low is 20/255, and default value for high is 50/255.
        :param int radius: Define the radius to search around an edge pixel for local maxima.
        :param int block_pct: Determine blurriness only for the most significant blocks, given in percentage.
        :param int block_width: Determine blurriness for blocks of width block_width. If set to any value smaller 1, no blocks are used and the whole image is processed as one no matter of block_height.
        :param int block_height: Determine blurriness for blocks of height block_height. If set to any value smaller 1, no blocks are used and the whole image is processed as one no matter of block_width.
        :param int planes: Set planes to filter. Default is first only.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#blurdetect

        """
        filter_node = FilterNode(
            name="blurdetect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "high": high,
                "low": low,
                "radius": radius,
                "block_pct": block_pct,
                "block_width": block_width,
                "block_height": block_height,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def boxblur(
        self,
        *,
        luma_radius: str | DefaultStr = DefaultStr("2"),
        luma_power: int | DefaultInt = DefaultInt(2),
        chroma_radius: str,
        chroma_power: int | DefaultInt = DefaultInt(-1),
        alpha_radius: str,
        alpha_power: int | DefaultInt = DefaultInt(-1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.19 boxblur
        Apply a boxblur algorithm to the input video.

        It accepts the following parameters:


        A description of the accepted options follows.

        Parameters:
        ----------

        :param str luma_radius: Set an expression for the box radius in pixels used for blurring the corresponding input plane. The radius value must be a non-negative number, and must not be greater than the value of the expression min(w,h)/2 for the luma and alpha planes, and of min(cw,ch)/2 for the chroma planes. Default value for luma_radius is "2". If not specified, chroma_radius and alpha_radius default to the corresponding value set for luma_radius. The expressions can contain the following constants: w h The input width and height in pixels. cw ch The input chroma image width and height in pixels. hsub vsub The horizontal and vertical chroma subsample values. For example, for the pixel format "yuv422p", hsub is 2 and vsub is 1.
        :param int luma_power: Specify how many times the boxblur filter is applied to the corresponding plane. Default value for luma_power is 2. If not specified, chroma_power and alpha_power default to the corresponding value set for luma_power. A value of 0 will disable the effect.
        :param str chroma_radius: Set an expression for the box radius in pixels used for blurring the corresponding input plane. The radius value must be a non-negative number, and must not be greater than the value of the expression min(w,h)/2 for the luma and alpha planes, and of min(cw,ch)/2 for the chroma planes. Default value for luma_radius is "2". If not specified, chroma_radius and alpha_radius default to the corresponding value set for luma_radius. The expressions can contain the following constants: w h The input width and height in pixels. cw ch The input chroma image width and height in pixels. hsub vsub The horizontal and vertical chroma subsample values. For example, for the pixel format "yuv422p", hsub is 2 and vsub is 1.
        :param int chroma_power: Specify how many times the boxblur filter is applied to the corresponding plane. Default value for luma_power is 2. If not specified, chroma_power and alpha_power default to the corresponding value set for luma_power. A value of 0 will disable the effect.
        :param str alpha_radius: Set an expression for the box radius in pixels used for blurring the corresponding input plane. The radius value must be a non-negative number, and must not be greater than the value of the expression min(w,h)/2 for the luma and alpha planes, and of min(cw,ch)/2 for the chroma planes. Default value for luma_radius is "2". If not specified, chroma_radius and alpha_radius default to the corresponding value set for luma_radius. The expressions can contain the following constants: w h The input width and height in pixels. cw ch The input chroma image width and height in pixels. hsub vsub The horizontal and vertical chroma subsample values. For example, for the pixel format "yuv422p", hsub is 2 and vsub is 1.
        :param int alpha_power: Specify how many times the boxblur filter is applied to the corresponding plane. Default value for luma_power is 2. If not specified, chroma_power and alpha_power default to the corresponding value set for luma_power. A value of 0 will disable the effect.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#boxblur

        """
        filter_node = FilterNode(
            name="boxblur",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "luma_radius": luma_radius,
                "luma_power": luma_power,
                "chroma_radius": chroma_radius,
                "chroma_power": chroma_power,
                "alpha_radius": alpha_radius,
                "alpha_power": alpha_power,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def boxblur_opencl(
        self,
        *,
        luma_radius: str | DefaultStr = DefaultStr("2"),
        luma_power: int | DefaultInt = DefaultInt(2),
        chroma_radius: str,
        chroma_power: int | DefaultInt = DefaultInt(-1),
        alpha_radius: str,
        alpha_power: int | DefaultInt = DefaultInt(-1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.2 boxblur_opencl
        Apply a boxblur algorithm to the input video.

        It accepts the following parameters:


        A description of the accepted options follows.

        Parameters:
        ----------

        :param str luma_radius: Set an expression for the box radius in pixels used for blurring the corresponding input plane. The radius value must be a non-negative number, and must not be greater than the value of the expression min(w,h)/2 for the luma and alpha planes, and of min(cw,ch)/2 for the chroma planes. Default value for luma_radius is "2". If not specified, chroma_radius and alpha_radius default to the corresponding value set for luma_radius. The expressions can contain the following constants: w h The input width and height in pixels. cw ch The input chroma image width and height in pixels. hsub vsub The horizontal and vertical chroma subsample values. For example, for the pixel format "yuv422p", hsub is 2 and vsub is 1.
        :param int luma_power: Specify how many times the boxblur filter is applied to the corresponding plane. Default value for luma_power is 2. If not specified, chroma_power and alpha_power default to the corresponding value set for luma_power. A value of 0 will disable the effect.
        :param str chroma_radius: Set an expression for the box radius in pixels used for blurring the corresponding input plane. The radius value must be a non-negative number, and must not be greater than the value of the expression min(w,h)/2 for the luma and alpha planes, and of min(cw,ch)/2 for the chroma planes. Default value for luma_radius is "2". If not specified, chroma_radius and alpha_radius default to the corresponding value set for luma_radius. The expressions can contain the following constants: w h The input width and height in pixels. cw ch The input chroma image width and height in pixels. hsub vsub The horizontal and vertical chroma subsample values. For example, for the pixel format "yuv422p", hsub is 2 and vsub is 1.
        :param int chroma_power: Specify how many times the boxblur filter is applied to the corresponding plane. Default value for luma_power is 2. If not specified, chroma_power and alpha_power default to the corresponding value set for luma_power. A value of 0 will disable the effect.
        :param str alpha_radius: Set an expression for the box radius in pixels used for blurring the corresponding input plane. The radius value must be a non-negative number, and must not be greater than the value of the expression min(w,h)/2 for the luma and alpha planes, and of min(cw,ch)/2 for the chroma planes. Default value for luma_radius is "2". If not specified, chroma_radius and alpha_radius default to the corresponding value set for luma_radius. The expressions can contain the following constants: w h The input width and height in pixels. cw ch The input chroma image width and height in pixels. hsub vsub The horizontal and vertical chroma subsample values. For example, for the pixel format "yuv422p", hsub is 2 and vsub is 1.
        :param int alpha_power: Specify how many times the boxblur filter is applied to the corresponding plane. Default value for luma_power is 2. If not specified, chroma_power and alpha_power default to the corresponding value set for luma_power. A value of 0 will disable the effect.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#boxblur_005fopencl

        """
        filter_node = FilterNode(
            name="boxblur_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "luma_radius": luma_radius,
                "luma_power": luma_power,
                "chroma_radius": chroma_radius,
                "chroma_power": chroma_power,
                "alpha_radius": alpha_radius,
                "alpha_power": alpha_power,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def bwdif(
        self,
        *,
        mode: int | Literal["send_frame", "send_field"] | DefaultStr = DefaultStr("send_field"),
        parity: int | Literal["tff", "bff", "auto"] | DefaultStr = DefaultStr("auto"),
        deint: int | Literal["all", "interlaced"] | DefaultStr = DefaultStr("all"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.20 bwdif
        Deinterlace the input video ("bwdif" stands for "Bob Weaver
        Deinterlacing Filter").

        Motion adaptive deinterlacing based on yadif with the use of w3fdif and cubic
        interpolation algorithms.
        It accepts the following parameters:

        Parameters:
        ----------

        :param int mode: The interlacing mode to adopt. It accepts one of the following values: 0, send_frame Output one frame for each frame. 1, send_field Output one frame for each field. The default value is send_field.
        :param int parity: The picture field parity assumed for the input interlaced video. It accepts one of the following values: 0, tff Assume the top field is first. 1, bff Assume the bottom field is first. -1, auto Enable automatic detection of field parity. The default value is auto. If the interlacing is unknown or the decoder does not export this information, top field first will be assumed.
        :param int deint: Specify which frames to deinterlace. Accepts one of the following values: 0, all Deinterlace all frames. 1, interlaced Only deinterlace frames marked as interlaced. The default value is all.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#bwdif

        """
        filter_node = FilterNode(
            name="bwdif",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "parity": parity,
                "deint": deint,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def bwdif_cuda(
        self,
        *,
        mode: int
        | Literal["send_frame", "send_field", "send_frame_nospatial", "send_field_nospatial"]
        | DefaultStr = DefaultStr("send_frame"),
        parity: int | Literal["tff", "bff", "auto"] | DefaultStr = DefaultStr("auto"),
        deint: int | Literal["all", "interlaced"] | DefaultStr = DefaultStr("all"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.21 bwdif_cuda
        Deinterlace the input video using the bwdif algorithm, but implemented
        in CUDA so that it can work as part of a GPU accelerated pipeline with nvdec
        and/or nvenc.

        It accepts the following parameters:

        Parameters:
        ----------

        :param int mode: The interlacing mode to adopt. It accepts one of the following values: 0, send_frame Output one frame for each frame. 1, send_field Output one frame for each field. The default value is send_field.
        :param int parity: The picture field parity assumed for the input interlaced video. It accepts one of the following values: 0, tff Assume the top field is first. 1, bff Assume the bottom field is first. -1, auto Enable automatic detection of field parity. The default value is auto. If the interlacing is unknown or the decoder does not export this information, top field first will be assumed.
        :param int deint: Specify which frames to deinterlace. Accepts one of the following values: 0, all Deinterlace all frames. 1, interlaced Only deinterlace frames marked as interlaced. The default value is all.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#bwdif_005fcuda

        """
        filter_node = FilterNode(
            name="bwdif_cuda",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "parity": parity,
                "deint": deint,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def bwdif_vulkan(
        self,
        *,
        mode: int
        | Literal["send_frame", "send_field", "send_frame_nospatial", "send_field_nospatial"]
        | DefaultStr = DefaultStr("send_frame"),
        parity: int | Literal["tff", "bff", "auto"] | DefaultStr = DefaultStr("auto"),
        deint: int | Literal["all", "interlaced"] | DefaultStr = DefaultStr("all"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        14.3 bwdif_vulkan
        Deinterlacer using bwdif, the "Bob Weaver Deinterlacing Filter" algorithm, implemented
        on the GPU using Vulkan.

        It accepts the following parameters:

        Parameters:
        ----------

        :param int mode: The interlacing mode to adopt. It accepts one of the following values: 0, send_frame Output one frame for each frame. 1, send_field Output one frame for each field. The default value is send_field.
        :param int parity: The picture field parity assumed for the input interlaced video. It accepts one of the following values: 0, tff Assume the top field is first. 1, bff Assume the bottom field is first. -1, auto Enable automatic detection of field parity. The default value is auto. If the interlacing is unknown or the decoder does not export this information, top field first will be assumed.
        :param int deint: Specify which frames to deinterlace. Accepts one of the following values: 0, all Deinterlace all frames. 1, interlaced Only deinterlace frames marked as interlaced. The default value is all.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#bwdif_005fvulkan

        """
        filter_node = FilterNode(
            name="bwdif_vulkan",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "parity": parity,
                "deint": deint,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def cas(
        self,
        *,
        strength: float | DefaultFloat = DefaultFloat(0.0),
        planes: str | DefaultStr = DefaultStr(7),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.23 cas
        Apply Contrast Adaptive Sharpen filter to video stream.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float strength: Set the sharpening strength. Default value is 0.
        :param str planes: Set planes to filter. Default value is to filter all planes except alpha plane.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#cas

        """
        filter_node = FilterNode(
            name="cas",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "strength": strength,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def ccrepack(self, **kwargs: Any) -> "VideoStream":
        """

        11.22 ccrepack
        Repack CEA-708 closed captioning side data

        This filter fixes various issues seen with commerical encoders
        related to upstream malformed CEA-708 payloads, specifically
        incorrect number of tuples (wrong cc_count for the target FPS),
        and incorrect ordering of tuples (i.e. the CEA-608 tuples are not at
        the first entries in the payload).

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#ccrepack

        """
        filter_node = FilterNode(
            name="ccrepack",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def chromaber_vulkan(
        self,
        *,
        dist_x: float | DefaultStr = DefaultStr("0.0f"),
        dist_y: float | DefaultStr = DefaultStr("0.0f"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        14.4 chromaber_vulkan
        Apply an effect that emulates chromatic aberration. Works best with RGB inputs,
        but provides a similar effect with YCbCr inputs too.

        Parameters:
        ----------

        :param float dist_x: Horizontal displacement multiplier. Each chroma pixel’s position will be multiplied by this amount, starting from the center of the image. Default is 0.
        :param float dist_y: Similarly, this sets the vertical displacement multiplier. Default is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#chromaber_005fvulkan

        """
        filter_node = FilterNode(
            name="chromaber_vulkan",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dist_x": dist_x,
                "dist_y": dist_y,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def chromahold(
        self,
        *,
        color: str | DefaultStr = DefaultStr("black"),
        similarity: float | DefaultFloat = DefaultFloat(0.01),
        blend: float | DefaultFloat = DefaultFloat(0.0),
        yuv: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.24 chromahold
        Remove all color information for all colors except for certain one.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str color: The color which will not be replaced with neutral chroma.
        :param float similarity: Similarity percentage with the above color. 0.01 matches only the exact key color, while 1.0 matches everything.
        :param float blend: Blend percentage. 0.0 makes pixels either fully gray, or not gray at all. Higher values result in more preserved color.
        :param bool yuv: Signals that the color passed is already in YUV instead of RGB. Literal colors like "green" or "red" don’t make sense with this enabled anymore. This can be used to pass exact YUV values as hexadecimal numbers.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#chromahold

        """
        filter_node = FilterNode(
            name="chromahold",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "color": color,
                "similarity": similarity,
                "blend": blend,
                "yuv": yuv,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def chromakey(
        self,
        *,
        color: str | DefaultStr = DefaultStr("black"),
        similarity: float | DefaultFloat = DefaultFloat(0.01),
        blend: float | DefaultFloat = DefaultFloat(0.0),
        yuv: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.25 chromakey
        YUV colorspace color/chroma keying.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str color: The color which will be replaced with transparency.
        :param float similarity: Similarity percentage with the key color. 0.01 matches only the exact key color, while 1.0 matches everything.
        :param float blend: Blend percentage. 0.0 makes pixels either fully transparent, or not transparent at all. Higher values result in semi-transparent pixels, with a higher transparency the more similar the pixels color is to the key color.
        :param bool yuv: Signals that the color passed is already in YUV instead of RGB. Literal colors like "green" or "red" don’t make sense with this enabled anymore. This can be used to pass exact YUV values as hexadecimal numbers.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#chromakey

        """
        filter_node = FilterNode(
            name="chromakey",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "color": color,
                "similarity": similarity,
                "blend": blend,
                "yuv": yuv,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def chromakey_cuda(
        self,
        *,
        color: str | DefaultStr = DefaultStr("black"),
        similarity: float | DefaultFloat = DefaultFloat(0.01),
        blend: float | DefaultFloat = DefaultFloat(0.0),
        yuv: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.26 chromakey_cuda
        CUDA accelerated YUV colorspace color/chroma keying.

        This filter works like normal chromakey filter but operates on CUDA frames.
        for more details and parameters see chromakey.

        Parameters:
        ----------

        :param str color: None
        :param float similarity: None
        :param float blend: None
        :param bool yuv: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#chromakey_005fcuda

        """
        filter_node = FilterNode(
            name="chromakey_cuda",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "color": color,
                "similarity": similarity,
                "blend": blend,
                "yuv": yuv,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def chromanr(
        self,
        *,
        thres: float | DefaultFloat = DefaultFloat(30.0),
        sizew: int | DefaultInt = DefaultInt(5),
        sizeh: int | DefaultInt = DefaultInt(5),
        stepw: int | DefaultInt = DefaultInt(1),
        steph: int | DefaultInt = DefaultInt(1),
        threy: float | DefaultFloat = DefaultFloat(200.0),
        threu: float | DefaultFloat = DefaultFloat(200.0),
        threv: float | DefaultFloat = DefaultFloat(200.0),
        distance: int | Literal["manhattan", "euclidean"] | DefaultStr = DefaultStr("manhattan"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.27 chromanr
        Reduce chrominance noise.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float thres: Set threshold for averaging chrominance values. Sum of absolute difference of Y, U and V pixel components of current pixel and neighbour pixels lower than this threshold will be used in averaging. Luma component is left unchanged and is copied to output. Default value is 30. Allowed range is from 1 to 200.
        :param int sizew: Set horizontal radius of rectangle used for averaging. Allowed range is from 1 to 100. Default value is 5.
        :param int sizeh: Set vertical radius of rectangle used for averaging. Allowed range is from 1 to 100. Default value is 5.
        :param int stepw: Set horizontal step when averaging. Default value is 1. Allowed range is from 1 to 50. Mostly useful to speed-up filtering.
        :param int steph: Set vertical step when averaging. Default value is 1. Allowed range is from 1 to 50. Mostly useful to speed-up filtering.
        :param float threy: Set Y threshold for averaging chrominance values. Set finer control for max allowed difference between Y components of current pixel and neigbour pixels. Default value is 200. Allowed range is from 1 to 200.
        :param float threu: Set U threshold for averaging chrominance values. Set finer control for max allowed difference between U components of current pixel and neigbour pixels. Default value is 200. Allowed range is from 1 to 200.
        :param float threv: Set V threshold for averaging chrominance values. Set finer control for max allowed difference between V components of current pixel and neigbour pixels. Default value is 200. Allowed range is from 1 to 200.
        :param int distance: Set distance type used in calculations. ‘manhattan’ Absolute difference. ‘euclidean’ Difference squared. Default distance type is manhattan.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#chromanr

        """
        filter_node = FilterNode(
            name="chromanr",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "thres": thres,
                "sizew": sizew,
                "sizeh": sizeh,
                "stepw": stepw,
                "steph": steph,
                "threy": threy,
                "threu": threu,
                "threv": threv,
                "distance": distance,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def chromashift(
        self,
        *,
        cbh: int | DefaultInt = DefaultInt(0),
        cbv: int | DefaultInt = DefaultInt(0),
        crh: int | DefaultInt = DefaultInt(0),
        crv: int | DefaultInt = DefaultInt(0),
        edge: int | Literal["smear", "wrap"] | DefaultStr = DefaultStr("smear"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.28 chromashift
        Shift chroma pixels horizontally and/or vertically.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int cbh: Set amount to shift chroma-blue horizontally.
        :param int cbv: Set amount to shift chroma-blue vertically.
        :param int crh: Set amount to shift chroma-red horizontally.
        :param int crv: Set amount to shift chroma-red vertically.
        :param int edge: Set edge mode, can be smear, default, or warp.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#chromashift

        """
        filter_node = FilterNode(
            name="chromashift",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "cbh": cbh,
                "cbv": cbv,
                "crh": crh,
                "crv": crv,
                "edge": edge,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def ciescope(
        self,
        *,
        system: int
        | Literal[
            "ntsc",
            "470m",
            "ebu",
            "470bg",
            "smpte",
            "240m",
            "apple",
            "widergb",
            "cie1931",
            "hdtv",
            "rec709",
            "uhdtv",
            "rec2020",
            "dcip3",
        ]
        | DefaultStr = DefaultStr("hdtv"),
        cie: int | Literal["xyy", "ucs", "luv"] | DefaultStr = DefaultStr("xyy"),
        gamuts: str
        | Literal[
            "ntsc",
            "470m",
            "ebu",
            "470bg",
            "smpte",
            "240m",
            "apple",
            "widergb",
            "cie1931",
            "hdtv",
            "rec709",
            "uhdtv",
            "rec2020",
            "dcip3",
        ]
        | DefaultStr = DefaultStr(0),
        size: int | DefaultInt = DefaultInt(512),
        intensity: float | DefaultFloat = DefaultFloat(0.001),
        contrast: float | DefaultFloat = DefaultFloat(0.75),
        corrgamma: bool | DefaultInt = DefaultInt(1),
        showwhite: bool | DefaultInt = DefaultInt(0),
        gamma: float | DefaultFloat = DefaultFloat(2.6),
        fill: bool | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.29 ciescope
        Display CIE color diagram with pixels overlaid onto it.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int system: Set color system. ‘ntsc, 470m’ ‘ebu, 470bg’ ‘smpte’ ‘240m’ ‘apple’ ‘widergb’ ‘cie1931’ ‘rec709, hdtv’ ‘uhdtv, rec2020’ ‘dcip3’
        :param int cie: Set CIE system. ‘xyy’ ‘ucs’ ‘luv’
        :param str gamuts: Set what gamuts to draw. See system option for available values.
        :param int size: Set ciescope size, by default set to 512.
        :param float intensity: Set intensity used to map input pixel values to CIE diagram.
        :param float contrast: Set contrast used to draw tongue colors that are out of active color system gamut.
        :param bool corrgamma: Correct gamma displayed on scope, by default enabled.
        :param bool showwhite: Show white point on CIE diagram, by default disabled.
        :param float gamma: Set input gamma. Used only with XYZ input color space.
        :param bool fill: Fill with CIE colors. By default is enabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#ciescope

        """
        filter_node = FilterNode(
            name="ciescope",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "system": system,
                "cie": cie,
                "gamuts": gamuts,
                "size": size,
                "intensity": intensity,
                "contrast": contrast,
                "corrgamma": corrgamma,
                "showwhite": showwhite,
                "gamma": gamma,
                "fill": fill,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def codecview(
        self,
        *,
        mv: str | Literal["pf", "bf", "bb"] | DefaultStr = DefaultStr(0),
        qp: bool | DefaultInt = DefaultInt(0),
        mv_type: str | Literal["fp", "bp"] | DefaultStr = DefaultStr(0),
        frame_type: str | Literal["if", "pf", "bf"] | DefaultStr = DefaultStr(0),
        block: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.30 codecview
        Visualize information exported by some codecs.

        Some codecs can export information through frames using side-data or other
        means. For example, some MPEG based codecs export motion vectors through the
        export_mvs flag in the codec flags2 option.

        The filter accepts the following option:

        Parameters:
        ----------

        :param str mv: Set motion vectors to visualize. Available flags for mv are: ‘pf’ forward predicted MVs of P-frames ‘bf’ forward predicted MVs of B-frames ‘bb’ backward predicted MVs of B-frames
        :param bool qp: Display quantization parameters using the chroma planes.
        :param str mv_type: Set motion vectors type to visualize. Includes MVs from all frames unless specified by frame_type option. Available flags for mv_type are: ‘fp’ forward predicted MVs ‘bp’ backward predicted MVs
        :param str frame_type: Set frame type to visualize motion vectors of. Available flags for frame_type are: ‘if’ intra-coded frames (I-frames) ‘pf’ predicted frames (P-frames) ‘bf’ bi-directionally predicted frames (B-frames)
        :param bool block: Display block partition structure using the luma plane.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#codecview

        """
        filter_node = FilterNode(
            name="codecview",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mv": mv,
                "qp": qp,
                "mv_type": mv_type,
                "frame_type": frame_type,
                "block": block,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorbalance(
        self,
        *,
        rs: float | DefaultFloat = DefaultFloat(0.0),
        gs: float | DefaultFloat = DefaultFloat(0.0),
        bs: float | DefaultFloat = DefaultFloat(0.0),
        rm: float | DefaultFloat = DefaultFloat(0.0),
        gm: float | DefaultFloat = DefaultFloat(0.0),
        bm: float | DefaultFloat = DefaultFloat(0.0),
        rh: float | DefaultFloat = DefaultFloat(0.0),
        gh: float | DefaultFloat = DefaultFloat(0.0),
        bh: float | DefaultFloat = DefaultFloat(0.0),
        pl: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.31 colorbalance
        Modify intensity of primary colors (red, green and blue) of input frames.

        The filter allows an input frame to be adjusted in the shadows, midtones or highlights
        regions for the red-cyan, green-magenta or blue-yellow balance.

        A positive adjustment value shifts the balance towards the primary color, a negative
        value towards the complementary color.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float rs: Adjust red, green and blue shadows (darkest pixels).
        :param float gs: Adjust red, green and blue shadows (darkest pixels).
        :param float bs: Adjust red, green and blue shadows (darkest pixels).
        :param float rm: Adjust red, green and blue midtones (medium pixels).
        :param float gm: Adjust red, green and blue midtones (medium pixels).
        :param float bm: Adjust red, green and blue midtones (medium pixels).
        :param float rh: Adjust red, green and blue highlights (brightest pixels). Allowed ranges for options are [-1.0, 1.0]. Defaults are 0.
        :param float gh: Adjust red, green and blue highlights (brightest pixels). Allowed ranges for options are [-1.0, 1.0]. Defaults are 0.
        :param float bh: Adjust red, green and blue highlights (brightest pixels). Allowed ranges for options are [-1.0, 1.0]. Defaults are 0.
        :param bool pl: Preserve lightness when changing color balance. Default is disabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorbalance

        """
        filter_node = FilterNode(
            name="colorbalance",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "rs": rs,
                "gs": gs,
                "bs": bs,
                "rm": rm,
                "gm": gm,
                "bm": bm,
                "rh": rh,
                "gh": gh,
                "bh": bh,
                "pl": pl,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorchannelmixer(
        self,
        *,
        rr: float | DefaultFloat = DefaultFloat(1.0),
        rg: float | DefaultFloat = DefaultFloat(0.0),
        rb: float | DefaultFloat = DefaultFloat(0.0),
        ra: float | DefaultFloat = DefaultFloat(0.0),
        gr: float | DefaultFloat = DefaultFloat(0.0),
        gg: float | DefaultFloat = DefaultFloat(1.0),
        gb: float | DefaultFloat = DefaultFloat(0.0),
        ga: float | DefaultFloat = DefaultFloat(0.0),
        br: float | DefaultFloat = DefaultFloat(0.0),
        bg: float | DefaultFloat = DefaultFloat(0.0),
        bb: float | DefaultFloat = DefaultFloat(1.0),
        ba: float | DefaultFloat = DefaultFloat(0.0),
        ar: float | DefaultFloat = DefaultFloat(0.0),
        ag: float | DefaultFloat = DefaultFloat(0.0),
        ab: float | DefaultFloat = DefaultFloat(0.0),
        aa: float | DefaultFloat = DefaultFloat(1.0),
        pc: int | Literal["none", "lum", "max", "avg", "sum", "nrm", "pwr"] | DefaultStr = DefaultStr(0),
        pa: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.34 colorchannelmixer
        Adjust video input frames by re-mixing color channels.

        This filter modifies a color channel by adding the values associated to
        the other channels of the same pixels. For example if the value to
        modify is red, the output value will be:

        red=red*rr + blue*rb + green*rg + alpha*ra

        The filter accepts the following options:

        Parameters:
        ----------

        :param float rr: Adjust contribution of input red, green, blue and alpha channels for output red channel. Default is 1 for rr, and 0 for rg, rb and ra.
        :param float rg: Adjust contribution of input red, green, blue and alpha channels for output red channel. Default is 1 for rr, and 0 for rg, rb and ra.
        :param float rb: Adjust contribution of input red, green, blue and alpha channels for output red channel. Default is 1 for rr, and 0 for rg, rb and ra.
        :param float ra: Adjust contribution of input red, green, blue and alpha channels for output red channel. Default is 1 for rr, and 0 for rg, rb and ra.
        :param float gr: Adjust contribution of input red, green, blue and alpha channels for output green channel. Default is 1 for gg, and 0 for gr, gb and ga.
        :param float gg: Adjust contribution of input red, green, blue and alpha channels for output green channel. Default is 1 for gg, and 0 for gr, gb and ga.
        :param float gb: Adjust contribution of input red, green, blue and alpha channels for output green channel. Default is 1 for gg, and 0 for gr, gb and ga.
        :param float ga: Adjust contribution of input red, green, blue and alpha channels for output green channel. Default is 1 for gg, and 0 for gr, gb and ga.
        :param float br: Adjust contribution of input red, green, blue and alpha channels for output blue channel. Default is 1 for bb, and 0 for br, bg and ba.
        :param float bg: Adjust contribution of input red, green, blue and alpha channels for output blue channel. Default is 1 for bb, and 0 for br, bg and ba.
        :param float bb: Adjust contribution of input red, green, blue and alpha channels for output blue channel. Default is 1 for bb, and 0 for br, bg and ba.
        :param float ba: Adjust contribution of input red, green, blue and alpha channels for output blue channel. Default is 1 for bb, and 0 for br, bg and ba.
        :param float ar: Adjust contribution of input red, green, blue and alpha channels for output alpha channel. Default is 1 for aa, and 0 for ar, ag and ab. Allowed ranges for options are [-2.0, 2.0].
        :param float ag: Adjust contribution of input red, green, blue and alpha channels for output alpha channel. Default is 1 for aa, and 0 for ar, ag and ab. Allowed ranges for options are [-2.0, 2.0].
        :param float ab: Adjust contribution of input red, green, blue and alpha channels for output alpha channel. Default is 1 for aa, and 0 for ar, ag and ab. Allowed ranges for options are [-2.0, 2.0].
        :param float aa: Adjust contribution of input red, green, blue and alpha channels for output alpha channel. Default is 1 for aa, and 0 for ar, ag and ab. Allowed ranges for options are [-2.0, 2.0].
        :param int pc: Set preserve color mode. The accepted values are: ‘none’ Disable color preserving, this is default. ‘lum’ Preserve luminance. ‘max’ Preserve max value of RGB triplet. ‘avg’ Preserve average value of RGB triplet. ‘sum’ Preserve sum value of RGB triplet. ‘nrm’ Preserve normalized value of RGB triplet. ‘pwr’ Preserve power value of RGB triplet.
        :param float pa: Set the preserve color amount when changing colors. Allowed range is from [0.0, 1.0]. Default is 0.0, thus disabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorchannelmixer

        """
        filter_node = FilterNode(
            name="colorchannelmixer",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "rr": rr,
                "rg": rg,
                "rb": rb,
                "ra": ra,
                "gr": gr,
                "gg": gg,
                "gb": gb,
                "ga": ga,
                "br": br,
                "bg": bg,
                "bb": bb,
                "ba": ba,
                "ar": ar,
                "ag": ag,
                "ab": ab,
                "aa": aa,
                "pc": pc,
                "pa": pa,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorcontrast(
        self,
        *,
        rc: float | DefaultFloat = DefaultFloat(0.0),
        gm: float | DefaultFloat = DefaultFloat(0.0),
        by: float | DefaultFloat = DefaultFloat(0.0),
        rcw: float | DefaultFloat = DefaultFloat(0.0),
        gmw: float | DefaultFloat = DefaultFloat(0.0),
        byw: float | DefaultFloat = DefaultFloat(0.0),
        pl: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.32 colorcontrast
        Adjust color contrast between RGB components.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float rc: Set the red-cyan contrast. Defaults is 0.0. Allowed range is from -1.0 to 1.0.
        :param float gm: Set the green-magenta contrast. Defaults is 0.0. Allowed range is from -1.0 to 1.0.
        :param float by: Set the blue-yellow contrast. Defaults is 0.0. Allowed range is from -1.0 to 1.0.
        :param float rcw: Set the weight of each rc, gm, by option value. Default value is 0.0. Allowed range is from 0.0 to 1.0. If all weights are 0.0 filtering is disabled.
        :param float gmw: Set the weight of each rc, gm, by option value. Default value is 0.0. Allowed range is from 0.0 to 1.0. If all weights are 0.0 filtering is disabled.
        :param float byw: Set the weight of each rc, gm, by option value. Default value is 0.0. Allowed range is from 0.0 to 1.0. If all weights are 0.0 filtering is disabled.
        :param float pl: Set the amount of preserving lightness. Default value is 0.0. Allowed range is from 0.0 to 1.0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorcontrast

        """
        filter_node = FilterNode(
            name="colorcontrast",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "rc": rc,
                "gm": gm,
                "by": by,
                "rcw": rcw,
                "gmw": gmw,
                "byw": byw,
                "pl": pl,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorcorrect(
        self,
        *,
        rl: float | DefaultFloat = DefaultFloat(0.0),
        bl: float | DefaultFloat = DefaultFloat(0.0),
        rh: float | DefaultFloat = DefaultFloat(0.0),
        bh: float | DefaultFloat = DefaultFloat(0.0),
        saturation: float | DefaultFloat = DefaultFloat(1.0),
        analyze: int | Literal["manual", "average", "minmax", "median"] | DefaultStr = DefaultStr(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.33 colorcorrect
        Adjust color white balance selectively for blacks and whites.
        This filter operates in YUV colorspace.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float rl: Set the red shadow spot. Allowed range is from -1.0 to 1.0. Default value is 0.
        :param float bl: Set the blue shadow spot. Allowed range is from -1.0 to 1.0. Default value is 0.
        :param float rh: Set the red highlight spot. Allowed range is from -1.0 to 1.0. Default value is 0.
        :param float bh: Set the blue highlight spot. Allowed range is from -1.0 to 1.0. Default value is 0.
        :param float saturation: Set the amount of saturation. Allowed range is from -3.0 to 3.0. Default value is 1.
        :param int analyze: If set to anything other than manual it will analyze every frame and use derived parameters for filtering output frame. Possible values are: ‘manual’ ‘average’ ‘minmax’ ‘median’ Default value is manual.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorcorrect

        """
        filter_node = FilterNode(
            name="colorcorrect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "rl": rl,
                "bl": bl,
                "rh": rh,
                "bh": bh,
                "saturation": saturation,
                "analyze": analyze,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorhold(
        self,
        *,
        color: str | DefaultStr = DefaultStr("black"),
        similarity: float | DefaultFloat = DefaultFloat(0.01),
        blend: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.37 colorhold
        Remove all color information for all RGB colors except for certain one.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str color: The color which will not be replaced with neutral gray.
        :param float similarity: Similarity percentage with the above color. 0.01 matches only the exact key color, while 1.0 matches everything.
        :param float blend: Blend percentage. 0.0 makes pixels fully gray. Higher values result in more preserved color.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorhold

        """
        filter_node = FilterNode(
            name="colorhold",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "color": color,
                "similarity": similarity,
                "blend": blend,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorize(
        self,
        *,
        hue: float | DefaultFloat = DefaultFloat(0.0),
        saturation: float | DefaultFloat = DefaultFloat(0.5),
        lightness: float | DefaultFloat = DefaultFloat(0.5),
        mix: float | DefaultFloat = DefaultFloat(1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.35 colorize
        Overlay a solid color on the video stream.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float hue: Set the color hue. Allowed range is from 0 to 360. Default value is 0.
        :param float saturation: Set the color saturation. Allowed range is from 0 to 1. Default value is 0.5.
        :param float lightness: Set the color lightness. Allowed range is from 0 to 1. Default value is 0.5.
        :param float mix: Set the mix of source lightness. By default is set to 1.0. Allowed range is from 0.0 to 1.0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorize

        """
        filter_node = FilterNode(
            name="colorize",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "hue": hue,
                "saturation": saturation,
                "lightness": lightness,
                "mix": mix,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorkey(
        self,
        *,
        color: str | DefaultStr = DefaultStr("black"),
        similarity: float | DefaultFloat = DefaultFloat(0.01),
        blend: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.36 colorkey
        RGB colorspace color keying.
        This filter operates on 8-bit RGB format frames by setting the alpha component of each pixel
        which falls within the similarity radius of the key color to 0. The alpha value for pixels outside
        the similarity radius depends on the value of the blend option.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str color: Set the color for which alpha will be set to 0 (full transparency). See (ffmpeg-utils)"Color" section in the ffmpeg-utils manual. Default is black.
        :param float similarity: Set the radius from the key color within which other colors also have full transparency. The computed distance is related to the unit fractional distance in 3D space between the RGB values of the key color and the pixel’s color. Range is 0.01 to 1.0. 0.01 matches within a very small radius around the exact key color, while 1.0 matches everything. Default is 0.01.
        :param float blend: Set how the alpha value for pixels that fall outside the similarity radius is computed. 0.0 makes pixels either fully transparent or fully opaque. Higher values result in semi-transparent pixels, with greater transparency the more similar the pixel color is to the key color. Range is 0.0 to 1.0. Default is 0.0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorkey

        """
        filter_node = FilterNode(
            name="colorkey",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "color": color,
                "similarity": similarity,
                "blend": blend,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorkey_opencl(
        self,
        *,
        color: str | DefaultStr = DefaultStr("black"),
        similarity: float | DefaultFloat = DefaultFloat(0.01),
        blend: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.3 colorkey_opencl
        RGB colorspace color keying.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str color: The color which will be replaced with transparency.
        :param float similarity: Similarity percentage with the key color. 0.01 matches only the exact key color, while 1.0 matches everything.
        :param float blend: Blend percentage. 0.0 makes pixels either fully transparent, or not transparent at all. Higher values result in semi-transparent pixels, with a higher transparency the more similar the pixels color is to the key color.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorkey_005fopencl

        """
        filter_node = FilterNode(
            name="colorkey_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "color": color,
                "similarity": similarity,
                "blend": blend,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorlevels(
        self,
        *,
        rimin: float | DefaultFloat = DefaultFloat(0.0),
        gimin: float | DefaultFloat = DefaultFloat(0.0),
        bimin: float | DefaultFloat = DefaultFloat(0.0),
        aimin: float | DefaultFloat = DefaultFloat(0.0),
        rimax: float | DefaultFloat = DefaultFloat(1.0),
        gimax: float | DefaultFloat = DefaultFloat(1.0),
        bimax: float | DefaultFloat = DefaultFloat(1.0),
        aimax: float | DefaultFloat = DefaultFloat(1.0),
        romin: float | DefaultFloat = DefaultFloat(0.0),
        gomin: float | DefaultFloat = DefaultFloat(0.0),
        bomin: float | DefaultFloat = DefaultFloat(0.0),
        aomin: float | DefaultFloat = DefaultFloat(0.0),
        romax: float | DefaultFloat = DefaultFloat(1.0),
        gomax: float | DefaultFloat = DefaultFloat(1.0),
        bomax: float | DefaultFloat = DefaultFloat(1.0),
        aomax: float | DefaultFloat = DefaultFloat(1.0),
        preserve: int | Literal["none", "lum", "max", "avg", "sum", "nrm", "pwr"] | DefaultStr = DefaultStr(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.38 colorlevels
        Adjust video input frames using levels.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float rimin: Adjust red, green, blue and alpha input black point. Allowed ranges for options are [-1.0, 1.0]. Defaults are 0.
        :param float gimin: Adjust red, green, blue and alpha input black point. Allowed ranges for options are [-1.0, 1.0]. Defaults are 0.
        :param float bimin: Adjust red, green, blue and alpha input black point. Allowed ranges for options are [-1.0, 1.0]. Defaults are 0.
        :param float aimin: Adjust red, green, blue and alpha input black point. Allowed ranges for options are [-1.0, 1.0]. Defaults are 0.
        :param float rimax: Adjust red, green, blue and alpha input white point. Allowed ranges for options are [-1.0, 1.0]. Defaults are 1. Input levels are used to lighten highlights (bright tones), darken shadows (dark tones), change the balance of bright and dark tones.
        :param float gimax: Adjust red, green, blue and alpha input white point. Allowed ranges for options are [-1.0, 1.0]. Defaults are 1. Input levels are used to lighten highlights (bright tones), darken shadows (dark tones), change the balance of bright and dark tones.
        :param float bimax: Adjust red, green, blue and alpha input white point. Allowed ranges for options are [-1.0, 1.0]. Defaults are 1. Input levels are used to lighten highlights (bright tones), darken shadows (dark tones), change the balance of bright and dark tones.
        :param float aimax: Adjust red, green, blue and alpha input white point. Allowed ranges for options are [-1.0, 1.0]. Defaults are 1. Input levels are used to lighten highlights (bright tones), darken shadows (dark tones), change the balance of bright and dark tones.
        :param float romin: Adjust red, green, blue and alpha output black point. Allowed ranges for options are [0, 1.0]. Defaults are 0.
        :param float gomin: Adjust red, green, blue and alpha output black point. Allowed ranges for options are [0, 1.0]. Defaults are 0.
        :param float bomin: Adjust red, green, blue and alpha output black point. Allowed ranges for options are [0, 1.0]. Defaults are 0.
        :param float aomin: Adjust red, green, blue and alpha output black point. Allowed ranges for options are [0, 1.0]. Defaults are 0.
        :param float romax: Adjust red, green, blue and alpha output white point. Allowed ranges for options are [0, 1.0]. Defaults are 1. Output levels allows manual selection of a constrained output level range.
        :param float gomax: Adjust red, green, blue and alpha output white point. Allowed ranges for options are [0, 1.0]. Defaults are 1. Output levels allows manual selection of a constrained output level range.
        :param float bomax: Adjust red, green, blue and alpha output white point. Allowed ranges for options are [0, 1.0]. Defaults are 1. Output levels allows manual selection of a constrained output level range.
        :param float aomax: Adjust red, green, blue and alpha output white point. Allowed ranges for options are [0, 1.0]. Defaults are 1. Output levels allows manual selection of a constrained output level range.
        :param int preserve: Set preserve color mode. The accepted values are: ‘none’ Disable color preserving, this is default. ‘lum’ Preserve luminance. ‘max’ Preserve max value of RGB triplet. ‘avg’ Preserve average value of RGB triplet. ‘sum’ Preserve sum value of RGB triplet. ‘nrm’ Preserve normalized value of RGB triplet. ‘pwr’ Preserve power value of RGB triplet.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorlevels

        """
        filter_node = FilterNode(
            name="colorlevels",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "rimin": rimin,
                "gimin": gimin,
                "bimin": bimin,
                "aimin": aimin,
                "rimax": rimax,
                "gimax": gimax,
                "bimax": bimax,
                "aimax": aimax,
                "romin": romin,
                "gomin": gomin,
                "bomin": bomin,
                "aomin": aomin,
                "romax": romax,
                "gomax": gomax,
                "bomax": bomax,
                "aomax": aomax,
                "preserve": preserve,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colormap(
        self,
        _source: "VideoStream",
        _target: "VideoStream",
        *,
        patch_size: str | DefaultStr = DefaultStr("64x64"),
        nb_patches: int | DefaultInt = DefaultInt(0),
        type: int | Literal["relative", "absolute"] | DefaultStr = DefaultStr("absolute"),
        kernel: int | Literal["euclidean", "weuclidean"] | DefaultStr = DefaultStr(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.39 colormap
        Apply custom color maps to video stream.

        This filter needs three input video streams.
        First stream is video stream that is going to be filtered out.
        Second and third video stream specify color patches for source
        color to target color mapping.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str patch_size: Set the source and target video stream patch size in pixels.
        :param int nb_patches: Set the max number of used patches from source and target video stream. Default value is number of patches available in additional video streams. Max allowed number of patches is 64.
        :param int type: Set the adjustments used for target colors. Can be relative or absolute. Defaults is absolute.
        :param int kernel: Set the kernel used to measure color differences between mapped colors. The accepted values are: ‘euclidean’ ‘weuclidean’ Default is euclidean.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colormap

        """
        filter_node = FilterNode(
            name="colormap",
            input_typings=[StreamType.video, StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _source,
                _target,
            ],
            kwargs={
                "patch_size": patch_size,
                "nb_patches": nb_patches,
                "type": type,
                "kernel": kernel,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colormatrix(
        self,
        *,
        src: int
        | Literal["bt709", "fcc", "bt601", "bt470", "bt470bg", "smpte170m", "smpte240m", "bt2020"]
        | DefaultStr = DefaultStr("COLOR_MODE_NONE"),
        dst: int
        | Literal["bt709", "fcc", "bt601", "bt470", "bt470bg", "smpte170m", "smpte240m", "bt2020"]
        | DefaultStr = DefaultStr("COLOR_MODE_NONE"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.40 colormatrix
        Convert color matrix.

        The filter accepts the following options:


        For example to convert from BT.601 to SMPTE-240M, use the command:

        colormatrix=bt601:smpte240m

        Parameters:
        ----------

        :param int src: Specify the source and destination color matrix. Both values must be specified. The accepted values are: ‘bt709’ BT.709 ‘fcc’ FCC ‘bt601’ BT.601 ‘bt470’ BT.470 ‘bt470bg’ BT.470BG ‘smpte170m’ SMPTE-170M ‘smpte240m’ SMPTE-240M ‘bt2020’ BT.2020
        :param int dst: Specify the source and destination color matrix. Both values must be specified. The accepted values are: ‘bt709’ BT.709 ‘fcc’ FCC ‘bt601’ BT.601 ‘bt470’ BT.470 ‘bt470bg’ BT.470BG ‘smpte170m’ SMPTE-170M ‘smpte240m’ SMPTE-240M ‘bt2020’ BT.2020

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colormatrix

        """
        filter_node = FilterNode(
            name="colormatrix",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "src": src,
                "dst": dst,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorspace(
        self,
        *,
        all: int
        | Literal["bt470m", "bt470bg", "bt601-6-525", "bt601-6-625", "bt709", "smpte170m", "smpte240m", "bt2020"]
        | DefaultStr = DefaultStr("CS_UNSPECIFIED"),
        space: int
        | Literal["bt709", "fcc", "bt470bg", "smpte170m", "smpte240m", "ycgco", "gbr", "bt2020nc", "bt2020ncl"]
        | DefaultStr = DefaultStr("AVCOL_SPC_UNSPECIFIED"),
        range: int | Literal["tv", "mpeg", "pc", "jpeg"] | DefaultStr = DefaultStr("AVCOL_RANGE_UNSPECIFIED"),
        primaries: int
        | Literal[
            "bt709",
            "bt470m",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "smpte428",
            "film",
            "smpte431",
            "smpte432",
            "bt2020",
            "jedec-p22",
            "ebu3213",
        ]
        | DefaultStr = DefaultStr("AVCOL_PRI_UNSPECIFIED"),
        trc: int
        | Literal[
            "bt709",
            "bt470m",
            "gamma22",
            "bt470bg",
            "gamma28",
            "smpte170m",
            "smpte240m",
            "linear",
            "srgb",
            "iec61966-2-1",
            "xvycc",
            "iec61966-2-4",
            "bt2020-10",
            "bt2020-12",
        ]
        | DefaultStr = DefaultStr("AVCOL_TRC_UNSPECIFIED"),
        format: int
        | Literal[
            "yuv420p",
            "yuv420p10",
            "yuv420p12",
            "yuv422p",
            "yuv422p10",
            "yuv422p12",
            "yuv444p",
            "yuv444p10",
            "yuv444p12",
        ]
        | DefaultStr = DefaultStr("AV_PIX_FMT_NONE"),
        fast: bool | DefaultInt = DefaultInt(0),
        dither: int | Literal["none", "fsb"] | DefaultStr = DefaultStr("none"),
        wpadapt: int | Literal["bradford", "vonkries", "identity"] | DefaultStr = DefaultStr("bradford"),
        iall: int
        | Literal["bt470m", "bt470bg", "bt601-6-525", "bt601-6-625", "bt709", "smpte170m", "smpte240m", "bt2020"]
        | DefaultStr = DefaultStr("CS_UNSPECIFIED"),
        ispace: int
        | Literal["bt709", "fcc", "bt470bg", "smpte170m", "smpte240m", "ycgco", "gbr", "bt2020nc", "bt2020ncl"]
        | DefaultStr = DefaultStr("AVCOL_SPC_UNSPECIFIED"),
        irange: int | Literal["tv", "mpeg", "pc", "jpeg"] | DefaultStr = DefaultStr("AVCOL_RANGE_UNSPECIFIED"),
        iprimaries: int
        | Literal[
            "bt709",
            "bt470m",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "smpte428",
            "film",
            "smpte431",
            "smpte432",
            "bt2020",
            "jedec-p22",
            "ebu3213",
        ]
        | DefaultStr = DefaultStr("AVCOL_PRI_UNSPECIFIED"),
        itrc: int
        | Literal[
            "bt709",
            "bt470m",
            "gamma22",
            "bt470bg",
            "gamma28",
            "smpte170m",
            "smpte240m",
            "linear",
            "srgb",
            "iec61966-2-1",
            "xvycc",
            "iec61966-2-4",
            "bt2020-10",
            "bt2020-12",
        ]
        | DefaultStr = DefaultStr("AVCOL_TRC_UNSPECIFIED"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.41 colorspace
        Convert colorspace, transfer characteristics or color primaries.
        Input video needs to have an even size.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int all: None
        :param int space: None
        :param int range: None
        :param int primaries: None
        :param int trc: None
        :param int format: None
        :param bool fast: None
        :param int dither: None
        :param int wpadapt: None
        :param int iall: None
        :param int ispace: None
        :param int irange: None
        :param int iprimaries: None
        :param int itrc: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorspace

        """
        filter_node = FilterNode(
            name="colorspace",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "all": all,
                "space": space,
                "range": range,
                "primaries": primaries,
                "trc": trc,
                "format": format,
                "fast": fast,
                "dither": dither,
                "wpadapt": wpadapt,
                "iall": iall,
                "ispace": ispace,
                "irange": irange,
                "iprimaries": iprimaries,
                "itrc": itrc,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colorspace_cuda(
        self,
        *,
        range: int | Literal["tv", "mpeg", "pc", "jpeg"] | DefaultStr = DefaultStr("AVCOL_RANGE_UNSPECIFIED"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.42 colorspace_cuda
        CUDA accelerated implementation of the colorspace filter.

        It is by no means feature complete compared to the software colorspace filter,
        and at the current time only supports color range conversion between jpeg/full
        and mpeg/limited range.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int range: Specify output color range. The accepted values are: ‘tv’ TV (restricted) range ‘mpeg’ MPEG (restricted) range ‘pc’ PC (full) range ‘jpeg’ JPEG (full) range

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colorspace_005fcuda

        """
        filter_node = FilterNode(
            name="colorspace_cuda",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "range": range,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def colortemperature(
        self,
        *,
        temperature: float | DefaultFloat = DefaultFloat(6500.0),
        mix: float | DefaultFloat = DefaultFloat(1.0),
        pl: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.43 colortemperature
        Adjust color temperature in video to simulate variations in ambient color temperature.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float temperature: Set the temperature in Kelvin. Allowed range is from 1000 to 40000. Default value is 6500 K.
        :param float mix: Set mixing with filtered output. Allowed range is from 0 to 1. Default value is 1.
        :param float pl: Set the amount of preserving lightness. Allowed range is from 0 to 1. Default value is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#colortemperature

        """
        filter_node = FilterNode(
            name="colortemperature",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "temperature": temperature,
                "mix": mix,
                "pl": pl,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def convolution(
        self,
        *,
        _0m: str | DefaultStr = DefaultStr("0 0 0 0 1 0 0 0 0"),
        _1m: str | DefaultStr = DefaultStr("0 0 0 0 1 0 0 0 0"),
        _2m: str | DefaultStr = DefaultStr("0 0 0 0 1 0 0 0 0"),
        _3m: str | DefaultStr = DefaultStr("0 0 0 0 1 0 0 0 0"),
        _0rdiv: float | DefaultFloat = DefaultFloat(0.0),
        _1rdiv: float | DefaultFloat = DefaultFloat(0.0),
        _2rdiv: float | DefaultFloat = DefaultFloat(0.0),
        _3rdiv: float | DefaultFloat = DefaultFloat(0.0),
        _0bias: float | DefaultFloat = DefaultFloat(0.0),
        _1bias: float | DefaultFloat = DefaultFloat(0.0),
        _2bias: float | DefaultFloat = DefaultFloat(0.0),
        _3bias: float | DefaultFloat = DefaultFloat(0.0),
        _0mode: int | Literal["square", "row", "column"] | DefaultStr = DefaultStr("square"),
        _1mode: int | Literal["square", "row", "column"] | DefaultStr = DefaultStr("square"),
        _2mode: int | Literal["square", "row", "column"] | DefaultStr = DefaultStr("square"),
        _3mode: int | Literal["square", "row", "column"] | DefaultStr = DefaultStr("square"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.44 convolution
        Apply convolution of 3x3, 5x5, 7x7 or horizontal/vertical up to 49 elements.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str _0m: Set matrix for each plane. Matrix is sequence of 9, 25 or 49 signed integers in square mode, and from 1 to 49 odd number of signed integers in row mode.
        :param str _1m: Set matrix for each plane. Matrix is sequence of 9, 25 or 49 signed integers in square mode, and from 1 to 49 odd number of signed integers in row mode.
        :param str _2m: Set matrix for each plane. Matrix is sequence of 9, 25 or 49 signed integers in square mode, and from 1 to 49 odd number of signed integers in row mode.
        :param str _3m: Set matrix for each plane. Matrix is sequence of 9, 25 or 49 signed integers in square mode, and from 1 to 49 odd number of signed integers in row mode.
        :param float _0rdiv: Set multiplier for calculated value for each plane. If unset or 0, it will be sum of all matrix elements.
        :param float _1rdiv: Set multiplier for calculated value for each plane. If unset or 0, it will be sum of all matrix elements.
        :param float _2rdiv: Set multiplier for calculated value for each plane. If unset or 0, it will be sum of all matrix elements.
        :param float _3rdiv: Set multiplier for calculated value for each plane. If unset or 0, it will be sum of all matrix elements.
        :param float _0bias: Set bias for each plane. This value is added to the result of the multiplication. Useful for making the overall image brighter or darker. Default is 0.0.
        :param float _1bias: Set bias for each plane. This value is added to the result of the multiplication. Useful for making the overall image brighter or darker. Default is 0.0.
        :param float _2bias: Set bias for each plane. This value is added to the result of the multiplication. Useful for making the overall image brighter or darker. Default is 0.0.
        :param float _3bias: Set bias for each plane. This value is added to the result of the multiplication. Useful for making the overall image brighter or darker. Default is 0.0.
        :param int _0mode: Set matrix mode for each plane. Can be square, row or column. Default is square.
        :param int _1mode: Set matrix mode for each plane. Can be square, row or column. Default is square.
        :param int _2mode: Set matrix mode for each plane. Can be square, row or column. Default is square.
        :param int _3mode: Set matrix mode for each plane. Can be square, row or column. Default is square.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#convolution

        """
        filter_node = FilterNode(
            name="convolution",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "0m": _0m,
                "1m": _1m,
                "2m": _2m,
                "3m": _3m,
                "0rdiv": _0rdiv,
                "1rdiv": _1rdiv,
                "2rdiv": _2rdiv,
                "3rdiv": _3rdiv,
                "0bias": _0bias,
                "1bias": _1bias,
                "2bias": _2bias,
                "3bias": _3bias,
                "0mode": _0mode,
                "1mode": _1mode,
                "2mode": _2mode,
                "3mode": _3mode,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def convolution_opencl(
        self,
        *,
        _0m: str | DefaultStr = DefaultStr("0 0 0 0 1 0 0 0 0"),
        _1m: str | DefaultStr = DefaultStr("0 0 0 0 1 0 0 0 0"),
        _2m: str | DefaultStr = DefaultStr("0 0 0 0 1 0 0 0 0"),
        _3m: str | DefaultStr = DefaultStr("0 0 0 0 1 0 0 0 0"),
        _0rdiv: float | DefaultFloat = DefaultFloat(1.0),
        _1rdiv: float | DefaultFloat = DefaultFloat(1.0),
        _2rdiv: float | DefaultFloat = DefaultFloat(1.0),
        _3rdiv: float | DefaultFloat = DefaultFloat(1.0),
        _0bias: float | DefaultFloat = DefaultFloat(0.0),
        _1bias: float | DefaultFloat = DefaultFloat(0.0),
        _2bias: float | DefaultFloat = DefaultFloat(0.0),
        _3bias: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.4 convolution_opencl
        Apply convolution of 3x3, 5x5, 7x7 matrix.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str _0m: Set matrix for each plane. Matrix is sequence of 9, 25 or 49 signed numbers. Default value for each plane is 0 0 0 0 1 0 0 0 0.
        :param str _1m: Set matrix for each plane. Matrix is sequence of 9, 25 or 49 signed numbers. Default value for each plane is 0 0 0 0 1 0 0 0 0.
        :param str _2m: Set matrix for each plane. Matrix is sequence of 9, 25 or 49 signed numbers. Default value for each plane is 0 0 0 0 1 0 0 0 0.
        :param str _3m: Set matrix for each plane. Matrix is sequence of 9, 25 or 49 signed numbers. Default value for each plane is 0 0 0 0 1 0 0 0 0.
        :param float _0rdiv: Set multiplier for calculated value for each plane. If unset or 0, it will be sum of all matrix elements. The option value must be a float number greater or equal to 0.0. Default value is 1.0.
        :param float _1rdiv: Set multiplier for calculated value for each plane. If unset or 0, it will be sum of all matrix elements. The option value must be a float number greater or equal to 0.0. Default value is 1.0.
        :param float _2rdiv: Set multiplier for calculated value for each plane. If unset or 0, it will be sum of all matrix elements. The option value must be a float number greater or equal to 0.0. Default value is 1.0.
        :param float _3rdiv: Set multiplier for calculated value for each plane. If unset or 0, it will be sum of all matrix elements. The option value must be a float number greater or equal to 0.0. Default value is 1.0.
        :param float _0bias: Set bias for each plane. This value is added to the result of the multiplication. Useful for making the overall image brighter or darker. The option value must be a float number greater or equal to 0.0. Default value is 0.0.
        :param float _1bias: Set bias for each plane. This value is added to the result of the multiplication. Useful for making the overall image brighter or darker. The option value must be a float number greater or equal to 0.0. Default value is 0.0.
        :param float _2bias: Set bias for each plane. This value is added to the result of the multiplication. Useful for making the overall image brighter or darker. The option value must be a float number greater or equal to 0.0. Default value is 0.0.
        :param float _3bias: Set bias for each plane. This value is added to the result of the multiplication. Useful for making the overall image brighter or darker. The option value must be a float number greater or equal to 0.0. Default value is 0.0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#convolution_005fopencl

        """
        filter_node = FilterNode(
            name="convolution_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "0m": _0m,
                "1m": _1m,
                "2m": _2m,
                "3m": _3m,
                "0rdiv": _0rdiv,
                "1rdiv": _1rdiv,
                "2rdiv": _2rdiv,
                "3rdiv": _3rdiv,
                "0bias": _0bias,
                "1bias": _1bias,
                "2bias": _2bias,
                "3bias": _3bias,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def convolve(
        self,
        _impulse: "VideoStream",
        *,
        planes: int | DefaultInt = DefaultInt(7),
        impulse: int | Literal["first", "all"] | DefaultStr = DefaultStr("all"),
        noise: float | DefaultFloat = DefaultFloat(1e-07),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.45 convolve
        Apply 2D convolution of video stream in frequency domain using second stream
        as impulse.

        The filter accepts the following options:


        The convolve filter also supports the framesync options.

        Parameters:
        ----------

        :param int planes: Set which planes to process.
        :param int impulse: Set which impulse video frames will be processed, can be first or all. Default is all.
        :param float noise: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#convolve

        """
        filter_node = FilterNode(
            name="convolve",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _impulse,
            ],
            kwargs={
                "planes": planes,
                "impulse": impulse,
                "noise": noise,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def copy(self, **kwargs: Any) -> "VideoStream":
        """

        11.46 copy
        Copy the input video source unchanged to the output. This is mainly useful for
        testing purposes.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#copy

        """
        filter_node = FilterNode(
            name="copy",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def coreimage(
        self,
        *,
        list_filters: bool | DefaultInt = DefaultInt(0),
        list_generators: bool | DefaultInt = DefaultInt(0),
        filter: str,
        output_rect: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.47 coreimage
        Video filtering on GPU using Apple’s CoreImage API on OSX.

        Hardware acceleration is based on an OpenGL context. Usually, this means it is
        processed by video hardware. However, software-based OpenGL implementations
        exist which means there is no guarantee for hardware processing. It depends on
        the respective OSX.

        There are many filters and image generators provided by Apple that come with a
        large variety of options. The filter has to be referenced by its name along
        with its options.

        The coreimage filter accepts the following options:

        Several filters can be chained for successive processing without GPU-HOST
        transfers allowing for fast processing of complex filter chains.
        Currently, only filters with zero (generators) or exactly one (filters) input
        image and one output image are supported. Also, transition filters are not yet
        usable as intended.

        Some filters generate output images with additional padding depending on the
        respective filter kernel. The padding is automatically removed to ensure the
        filter output has the same size as the input image.

        For image generators, the size of the output image is determined by the
        previous output image of the filter chain or the input image of the whole
        filterchain, respectively. The generators do not use the pixel information of
        this image to generate their output. However, the generated output is
        blended onto this image, resulting in partial or complete coverage of the
        output image.

        The coreimagesrc video source can be used for generating input images
        which are directly fed into the filter chain. By using it, providing input
        images by another video source or an input video is not required.

        Parameters:
        ----------

        :param bool list_filters: List all available filters and generators along with all their respective options as well as possible minimum and maximum values along with the default values. list_filters=true
        :param bool list_generators: None
        :param str filter: Specify all filters by their respective name and options. Use list_filters to determine all valid filter names and options. Numerical options are specified by a float value and are automatically clamped to their respective value range. Vector and color options have to be specified by a list of space separated float values. Character escaping has to be done. A special option name default is available to use default options for a filter. It is required to specify either default or at least one of the filter options. All omitted options are used with their default values. The syntax of the filter string is as follows: filter=<NAME>@<OPTION>=<VALUE>[@<OPTION>=<VALUE>][@...][#<NAME>@<OPTION>=<VALUE>[@<OPTION>=<VALUE>][@...]][#...]
        :param str output_rect: Specify a rectangle where the output of the filter chain is copied into the input image. It is given by a list of space separated float values: output_rect=x\ y\ width\ height If not given, the output rectangle equals the dimensions of the input image. The output rectangle is automatically cropped at the borders of the input image. Negative values are valid for each component. output_rect=25\ 25\ 100\ 100

        Ref: https://ffmpeg.org/ffmpeg-filters.html#coreimage

        """
        filter_node = FilterNode(
            name="coreimage",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "list_filters": list_filters,
                "list_generators": list_generators,
                "filter": filter,
                "output_rect": output_rect,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def corr(self, _reference: "VideoStream", **kwargs: Any) -> "VideoStream":
        """

        11.48 corr
        Obtain the correlation between two input videos.

        This filter takes two input videos.

        Both input videos must have the same resolution and pixel format for
        this filter to work correctly. Also it assumes that both inputs
        have the same number of frames, which are compared one by one.

        The obtained per component, average, min and max correlation is printed through
        the logging system.

        The filter stores the calculated correlation of each frame in frame metadata.

        This filter also supports the framesync options.

        In the below example the input file main.mpg being processed is compared
        with the reference file ref.mpg.


        ffmpeg -i main.mpg -i ref.mpg -lavfi corr -f null -

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#corr

        """
        filter_node = FilterNode(
            name="corr",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _reference,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def cover_rect(
        self, *, cover: str, mode: int | Literal["cover", "blur"] | DefaultStr = DefaultStr("blur"), **kwargs: Any
    ) -> "VideoStream":
        """

        11.49 cover_rect
        Cover a rectangular object

        It accepts the following options:

        Parameters:
        ----------

        :param str cover: Filepath of the optional cover image, needs to be in yuv420.
        :param int mode: Set covering mode. It accepts the following values: ‘cover’ cover it by the supplied image ‘blur’ cover it by interpolating the surrounding pixels Default value is blur.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#cover_005frect

        """
        filter_node = FilterNode(
            name="cover_rect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "cover": cover,
                "mode": mode,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def crop(
        self,
        *,
        out_w: str | DefaultStr = DefaultStr("iw"),
        out_h: str | DefaultStr = DefaultStr("ih"),
        x: str | DefaultStr = DefaultStr("(in_w-out_w)/2"),
        y: str | DefaultStr = DefaultStr("(in_h-out_h)/2"),
        keep_aspect: bool | DefaultInt = DefaultInt(0),
        exact: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.50 crop
        Crop the input video to given dimensions.

        It accepts the following parameters:


        The out_w, out_h, x, y parameters are
        expressions containing the following constants:


        The expression for out_w may depend on the value of out_h,
        and the expression for out_h may depend on out_w, but they
        cannot depend on x and y, as x and y are
        evaluated after out_w and out_h.

        The x and y parameters specify the expressions for the
        position of the top-left corner of the output (non-cropped) area. They
        are evaluated for each frame. If the evaluated value is not valid, it
        is approximated to the nearest valid value.

        The expression for x may depend on y, and the expression
        for y may depend on x.

        Parameters:
        ----------

        :param str out_w: The width of the output video. It defaults to iw. This expression is evaluated only once during the filter configuration, or when the ‘w’ or ‘out_w’ command is sent.
        :param str out_h: The height of the output video. It defaults to ih. This expression is evaluated only once during the filter configuration, or when the ‘h’ or ‘out_h’ command is sent.
        :param str x: The horizontal position, in the input video, of the left edge of the output video. It defaults to (in_w-out_w)/2. This expression is evaluated per-frame.
        :param str y: The vertical position, in the input video, of the top edge of the output video. It defaults to (in_h-out_h)/2. This expression is evaluated per-frame.
        :param bool keep_aspect: If set to 1 will force the output display aspect ratio to be the same of the input, by changing the output sample aspect ratio. It defaults to 0.
        :param bool exact: Enable exact cropping. If enabled, subsampled videos will be cropped at exact width/height/x/y as specified and will not be rounded to nearest smaller value. It defaults to 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#crop

        """
        filter_node = FilterNode(
            name="crop",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "out_w": out_w,
                "out_h": out_h,
                "x": x,
                "y": y,
                "keep_aspect": keep_aspect,
                "exact": exact,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def cropdetect(
        self,
        *,
        limit: float | DefaultStr = DefaultStr("24.0/255"),
        round: int | DefaultInt = DefaultInt(16),
        reset: int | DefaultInt = DefaultInt(0),
        skip: int | DefaultInt = DefaultInt(2),
        max_outliers: int | DefaultInt = DefaultInt(0),
        mode: int | Literal["black", "mvedges"] | DefaultStr = DefaultStr("black"),
        high: float | DefaultStr = DefaultStr("25/255."),
        low: float | DefaultStr = DefaultStr("15/255."),
        mv_threshold: int | DefaultInt = DefaultInt(8),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.51 cropdetect
        Auto-detect the crop size.

        It calculates the necessary cropping parameters and prints the
        recommended parameters via the logging system. The detected dimensions
        correspond to the non-black or video area of the input video according to mode.

        It accepts the following parameters:

        Parameters:
        ----------

        :param float limit: Set higher black value threshold, which can be optionally specified from nothing (0) to everything (255 for 8-bit based formats). An intensity value greater to the set value is considered non-black. It defaults to 24. You can also specify a value between 0.0 and 1.0 which will be scaled depending on the bitdepth of the pixel format.
        :param int round: The value which the width/height should be divisible by. It defaults to 16. The offset is automatically adjusted to center the video. Use 2 to get only even dimensions (needed for 4:2:2 video). 16 is best when encoding to most video codecs.
        :param int reset: Set the counter that determines after how many frames cropdetect will reset the previously detected largest video area and start over to detect the current optimal crop area. Default value is 0. This can be useful when channel logos distort the video area. 0 indicates ’never reset’, and returns the largest area encountered during playback.
        :param int skip: Set the number of initial frames for which evaluation is skipped. Default is 2. Range is 0 to INT_MAX.
        :param int max_outliers: None
        :param int mode: Depending on mode crop detection is based on either the mere black value of surrounding pixels or a combination of motion vectors and edge pixels. ‘black’ Detect black pixels surrounding the playing video. For fine control use option limit. ‘mvedges’ Detect the playing video by the motion vectors inside the video and scanning for edge pixels typically forming the border of a playing video.
        :param float high: Set low and high threshold values used by the Canny thresholding algorithm. The high threshold selects the "strong" edge pixels, which are then connected through 8-connectivity with the "weak" edge pixels selected by the low threshold. low and high threshold values must be chosen in the range [0,1], and low should be lesser or equal to high. Default value for low is 5/255, and default value for high is 15/255.
        :param float low: Set low and high threshold values used by the Canny thresholding algorithm. The high threshold selects the "strong" edge pixels, which are then connected through 8-connectivity with the "weak" edge pixels selected by the low threshold. low and high threshold values must be chosen in the range [0,1], and low should be lesser or equal to high. Default value for low is 5/255, and default value for high is 15/255.
        :param int mv_threshold: Set motion in pixel units as threshold for motion detection. It defaults to 8.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#cropdetect

        """
        filter_node = FilterNode(
            name="cropdetect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "limit": limit,
                "round": round,
                "reset": reset,
                "skip": skip,
                "max_outliers": max_outliers,
                "mode": mode,
                "high": high,
                "low": low,
                "mv_threshold": mv_threshold,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def cue(
        self,
        *,
        cue: int | DefaultInt = DefaultInt(0),
        preroll: int | DefaultInt = DefaultInt(0),
        buffer: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.52 cue
        Delay video filtering until a given wallclock timestamp. The filter first
        passes on preroll amount of frames, then it buffers at most
        buffer amount of frames and waits for the cue. After reaching the cue
        it forwards the buffered frames and also any subsequent frames coming in its
        input.

        The filter can be used synchronize the output of multiple ffmpeg processes for
        realtime output devices like decklink. By putting the delay in the filtering
        chain and pre-buffering frames the process can pass on data to output almost
        immediately after the target wallclock timestamp is reached.

        Perfect frame accuracy cannot be guaranteed, but the result is good enough for
        some use cases.

        Parameters:
        ----------

        :param int cue: The cue timestamp expressed in a UNIX timestamp in microseconds. Default is 0.
        :param int preroll: The duration of content to pass on as preroll expressed in seconds. Default is 0.
        :param int buffer: The maximum duration of content to buffer before waiting for the cue expressed in seconds. Default is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#cue

        """
        filter_node = FilterNode(
            name="cue",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "cue": cue,
                "preroll": preroll,
                "buffer": buffer,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def curves(
        self,
        *,
        preset: int
        | Literal[
            "none",
            "color_negative",
            "cross_process",
            "darker",
            "increase_contrast",
            "lighter",
            "linear_contrast",
            "medium_contrast",
            "negative",
            "strong_contrast",
            "vintage",
        ]
        | DefaultStr = DefaultStr("none"),
        master: str,
        red: str,
        green: str,
        blue: str,
        all: str,
        psfile: str,
        plot: str,
        interp: int | Literal["natural", "pchip"] | DefaultStr = DefaultStr("natural"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.53 curves
        Apply color adjustments using curves.

        This filter is similar to the Adobe Photoshop and GIMP curves tools. Each
        component (red, green and blue) has its values defined by N key points
        tied from each other using a smooth curve. The x-axis represents the pixel
        values from the input frame, and the y-axis the new pixel values to be set for
        the output frame.

        By default, a component curve is defined by the two points (0;0) and
        (1;1). This creates a straight line where each original pixel value is
        "adjusted" to its own value, which means no change to the image.

        The filter allows you to redefine these two points and add some more. A new
        curve will be define to pass smoothly through all these new coordinates. The
        new defined points needs to be strictly increasing over the x-axis, and their
        x and y values must be in the [0;1] interval. The curve is
        formed by using a natural or monotonic cubic spline interpolation, depending
        on the interp option (default: natural). The natural
        spline produces a smoother curve in general while the monotonic (pchip)
        spline guarantees the transitions between the specified points to be
        monotonic. If the computed curves happened to go outside the vector spaces,
        the values will be clipped accordingly.

        The filter accepts the following options:


        To avoid some filtergraph syntax conflicts, each key points list need to be
        defined using the following syntax: x0/y0 x1/y1 x2/y2 ....

        Parameters:
        ----------

        :param int preset: Select one of the available color presets. This option can be used in addition to the r, g, b parameters; in this case, the later options takes priority on the preset values. Available presets are: ‘none’ ‘color_negative’ ‘cross_process’ ‘darker’ ‘increase_contrast’ ‘lighter’ ‘linear_contrast’ ‘medium_contrast’ ‘negative’ ‘strong_contrast’ ‘vintage’ Default is none.
        :param str master: Set the master key points. These points will define a second pass mapping. It is sometimes called a "luminance" or "value" mapping. It can be used with r, g, b or all since it acts like a post-processing LUT.
        :param str red: Set the key points for the red component.
        :param str green: Set the key points for the green component.
        :param str blue: Set the key points for the blue component.
        :param str all: Set the key points for all components (not including master). Can be used in addition to the other key points component options. In this case, the unset component(s) will fallback on this all setting.
        :param str psfile: Specify a Photoshop curves file (.acv) to import the settings from.
        :param str plot: Save Gnuplot script of the curves in specified file.
        :param int interp: Specify the kind of interpolation. Available algorithms are: ‘natural’ Natural cubic spline using a piece-wise cubic polynomial that is twice continuously differentiable. ‘pchip’ Monotonic cubic spline using a piecewise cubic Hermite interpolating polynomial (PCHIP).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#curves

        """
        filter_node = FilterNode(
            name="curves",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "preset": preset,
                "master": master,
                "red": red,
                "green": green,
                "blue": blue,
                "all": all,
                "psfile": psfile,
                "plot": plot,
                "interp": interp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def datascope(
        self,
        *,
        size: str | DefaultStr = DefaultStr("hd720"),
        x: int | DefaultInt = DefaultInt(0),
        y: int | DefaultInt = DefaultInt(0),
        mode: int | Literal["mono", "color", "color2"] | DefaultStr = DefaultStr("mono"),
        axis: bool | DefaultInt = DefaultInt(0),
        opacity: float | DefaultFloat = DefaultFloat(0.75),
        format: int | Literal["hex", "dec"] | DefaultStr = DefaultStr("hex"),
        components: int | DefaultInt = DefaultInt(15),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.54 datascope
        Video data analysis filter.

        This filter shows hexadecimal pixel values of part of video.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str size: Set output video size.
        :param int x: Set x offset from where to pick pixels.
        :param int y: Set y offset from where to pick pixels.
        :param int mode: Set scope mode, can be one of the following: ‘mono’ Draw hexadecimal pixel values with white color on black background. ‘color’ Draw hexadecimal pixel values with input video pixel color on black background. ‘color2’ Draw hexadecimal pixel values on color background picked from input video, the text color is picked in such way so its always visible.
        :param bool axis: Draw rows and columns numbers on left and top of video.
        :param float opacity: Set background opacity.
        :param int format: Set display number format. Can be hex, or dec. Default is hex.
        :param int components: Set pixel components to display. By default all pixel components are displayed.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#datascope

        """
        filter_node = FilterNode(
            name="datascope",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "size": size,
                "x": x,
                "y": y,
                "mode": mode,
                "axis": axis,
                "opacity": opacity,
                "format": format,
                "components": components,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def dblur(
        self,
        *,
        angle: float | DefaultFloat = DefaultFloat(45.0),
        radius: float | DefaultFloat = DefaultFloat(5.0),
        planes: int | DefaultStr = DefaultStr("0xF"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.55 dblur
        Apply Directional blur filter.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float angle: Set angle of directional blur. Default is 45.
        :param float radius: Set radius of directional blur. Default is 5.
        :param int planes: Set which planes to filter. By default all planes are filtered.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#dblur

        """
        filter_node = FilterNode(
            name="dblur",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "angle": angle,
                "radius": radius,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def dctdnoiz(
        self,
        *,
        sigma: float | DefaultFloat = DefaultFloat(0.0),
        overlap: int | DefaultInt = DefaultInt(-1),
        expr: str,
        n: int | DefaultInt = DefaultInt(3),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.56 dctdnoiz
        Denoise frames using 2D DCT (frequency domain filtering).

        This filter is not designed for real time.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float sigma: Set the noise sigma constant. This sigma defines a hard threshold of 3 * sigma; every DCT coefficient (absolute value) below this threshold with be dropped. If you need a more advanced filtering, see expr. Default is 0.
        :param int overlap: Set number overlapping pixels for each block. Since the filter can be slow, you may want to reduce this value, at the cost of a less effective filter and the risk of various artefacts. If the overlapping value doesn’t permit processing the whole input width or height, a warning will be displayed and according borders won’t be denoised. Default value is blocksize-1, which is the best possible setting.
        :param str expr: Set the coefficient factor expression. For each coefficient of a DCT block, this expression will be evaluated as a multiplier value for the coefficient. If this is option is set, the sigma option will be ignored. The absolute value of the coefficient can be accessed through the c variable.
        :param int n: Set the blocksize using the number of bits. 1<<n defines the blocksize, which is the width and height of the processed blocks. The default value is 3 (8x8) and can be raised to 4 for a blocksize of 16x16. Note that changing this setting has huge consequences on the speed processing. Also, a larger block size does not necessarily means a better de-noising.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#dctdnoiz

        """
        filter_node = FilterNode(
            name="dctdnoiz",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "sigma": sigma,
                "overlap": overlap,
                "expr": expr,
                "n": n,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def deband(
        self,
        *,
        _1thr: float | DefaultFloat = DefaultFloat(0.02),
        _2thr: float | DefaultFloat = DefaultFloat(0.02),
        _3thr: float | DefaultFloat = DefaultFloat(0.02),
        _4thr: float | DefaultFloat = DefaultFloat(0.02),
        range: int | DefaultInt = DefaultInt(16),
        direction: float | DefaultStr = DefaultStr("2*3.14159265358979323846264338327950288"),
        blur: bool | DefaultInt = DefaultInt(1),
        coupling: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.57 deband
        Remove banding artifacts from input video.
        It works by replacing banded pixels with average value of referenced pixels.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float _1thr: Set banding detection threshold for each plane. Default is 0.02. Valid range is 0.00003 to 0.5. If difference between current pixel and reference pixel is less than threshold, it will be considered as banded.
        :param float _2thr: Set banding detection threshold for each plane. Default is 0.02. Valid range is 0.00003 to 0.5. If difference between current pixel and reference pixel is less than threshold, it will be considered as banded.
        :param float _3thr: Set banding detection threshold for each plane. Default is 0.02. Valid range is 0.00003 to 0.5. If difference between current pixel and reference pixel is less than threshold, it will be considered as banded.
        :param float _4thr: Set banding detection threshold for each plane. Default is 0.02. Valid range is 0.00003 to 0.5. If difference between current pixel and reference pixel is less than threshold, it will be considered as banded.
        :param int range: Banding detection range in pixels. Default is 16. If positive, random number in range 0 to set value will be used. If negative, exact absolute value will be used. The range defines square of four pixels around current pixel.
        :param float direction: Set direction in radians from which four pixel will be compared. If positive, random direction from 0 to set direction will be picked. If negative, exact of absolute value will be picked. For example direction 0, -PI or -2*PI radians will pick only pixels on same row and -PI/2 will pick only pixels on same column.
        :param bool blur: If enabled, current pixel is compared with average value of all four surrounding pixels. The default is enabled. If disabled current pixel is compared with all four surrounding pixels. The pixel is considered banded if only all four differences with surrounding pixels are less than threshold.
        :param bool coupling: If enabled, current pixel is changed if and only if all pixel components are banded, e.g. banding detection threshold is triggered for all color components. The default is disabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#deband

        """
        filter_node = FilterNode(
            name="deband",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "1thr": _1thr,
                "2thr": _2thr,
                "3thr": _3thr,
                "4thr": _4thr,
                "range": range,
                "direction": direction,
                "blur": blur,
                "coupling": coupling,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def deblock(
        self,
        *,
        filter: int | Literal["weak", "strong"] | DefaultStr = DefaultStr("strong"),
        block: int | DefaultInt = DefaultInt(8),
        alpha: float | DefaultFloat = DefaultFloat(0.098),
        beta: float | DefaultFloat = DefaultFloat(0.05),
        gamma: float | DefaultFloat = DefaultFloat(0.05),
        delta: float | DefaultFloat = DefaultFloat(0.05),
        planes: int | DefaultInt = DefaultInt(15),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.58 deblock
        Remove blocking artifacts from input video.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int filter: Set filter type, can be weak or strong. Default is strong. This controls what kind of deblocking is applied.
        :param int block: Set size of block, allowed range is from 4 to 512. Default is 8.
        :param float alpha: Set blocking detection thresholds. Allowed range is 0 to 1. Defaults are: 0.098 for alpha and 0.05 for the rest. Using higher threshold gives more deblocking strength. Setting alpha controls threshold detection at exact edge of block. Remaining options controls threshold detection near the edge. Each one for below/above or left/right. Setting any of those to 0 disables deblocking.
        :param float beta: Set blocking detection thresholds. Allowed range is 0 to 1. Defaults are: 0.098 for alpha and 0.05 for the rest. Using higher threshold gives more deblocking strength. Setting alpha controls threshold detection at exact edge of block. Remaining options controls threshold detection near the edge. Each one for below/above or left/right. Setting any of those to 0 disables deblocking.
        :param float gamma: Set blocking detection thresholds. Allowed range is 0 to 1. Defaults are: 0.098 for alpha and 0.05 for the rest. Using higher threshold gives more deblocking strength. Setting alpha controls threshold detection at exact edge of block. Remaining options controls threshold detection near the edge. Each one for below/above or left/right. Setting any of those to 0 disables deblocking.
        :param float delta: Set blocking detection thresholds. Allowed range is 0 to 1. Defaults are: 0.098 for alpha and 0.05 for the rest. Using higher threshold gives more deblocking strength. Setting alpha controls threshold detection at exact edge of block. Remaining options controls threshold detection near the edge. Each one for below/above or left/right. Setting any of those to 0 disables deblocking.
        :param int planes: Set planes to filter. Default is to filter all available planes.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#deblock

        """
        filter_node = FilterNode(
            name="deblock",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "filter": filter,
                "block": block,
                "alpha": alpha,
                "beta": beta,
                "gamma": gamma,
                "delta": delta,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def deconvolve(
        self,
        _impulse: "VideoStream",
        *,
        planes: int | DefaultInt = DefaultInt(7),
        impulse: int | Literal["first", "all"] | DefaultStr = DefaultStr("all"),
        noise: float | DefaultFloat = DefaultFloat(1e-07),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.60 deconvolve
        Apply 2D deconvolution of video stream in frequency domain using second stream
        as impulse.

        The filter accepts the following options:


        The deconvolve filter also supports the framesync options.

        Parameters:
        ----------

        :param int planes: Set which planes to process.
        :param int impulse: Set which impulse video frames will be processed, can be first or all. Default is all.
        :param float noise: Set noise when doing divisions. Default is 0.0000001. Useful when width and height are not same and not power of 2 or if stream prior to convolving had noise.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#deconvolve

        """
        filter_node = FilterNode(
            name="deconvolve",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _impulse,
            ],
            kwargs={
                "planes": planes,
                "impulse": impulse,
                "noise": noise,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def dedot(
        self,
        *,
        m: str | Literal["dotcrawl", "rainbows"] | DefaultStr = DefaultStr(3),
        lt: float | DefaultFloat = DefaultFloat(0.079),
        tl: float | DefaultFloat = DefaultFloat(0.079),
        tc: float | DefaultFloat = DefaultFloat(0.058),
        ct: float | DefaultFloat = DefaultFloat(0.019),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.61 dedot
        Reduce cross-luminance (dot-crawl) and cross-color (rainbows) from video.

        It accepts the following options:

        Parameters:
        ----------

        :param str m: Set mode of operation. Can be combination of dotcrawl for cross-luminance reduction and/or rainbows for cross-color reduction.
        :param float lt: Set spatial luma threshold. Lower values increases reduction of cross-luminance.
        :param float tl: Set tolerance for temporal luma. Higher values increases reduction of cross-luminance.
        :param float tc: Set tolerance for chroma temporal variation. Higher values increases reduction of cross-color.
        :param float ct: Set temporal chroma threshold. Lower values increases reduction of cross-color.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#dedot

        """
        filter_node = FilterNode(
            name="dedot",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "m": m,
                "lt": lt,
                "tl": tl,
                "tc": tc,
                "ct": ct,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def deflate(
        self,
        *,
        threshold0: int | DefaultInt = DefaultInt(65535),
        threshold1: int | DefaultInt = DefaultInt(65535),
        threshold2: int | DefaultInt = DefaultInt(65535),
        threshold3: int | DefaultInt = DefaultInt(65535),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.62 deflate
        Apply deflate effect to the video.

        This filter replaces the pixel by the local(3x3) average by taking into account
        only values lower than the pixel.

        It accepts the following options:

        Parameters:
        ----------

        :param int threshold0: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold1: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold2: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold3: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#deflate

        """
        filter_node = FilterNode(
            name="deflate",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "threshold0": threshold0,
                "threshold1": threshold1,
                "threshold2": threshold2,
                "threshold3": threshold3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def deflicker(
        self,
        *,
        size: int | DefaultInt = DefaultInt(5),
        mode: int | Literal["am", "gm", "hm", "qm", "cm", "pm", "median"] | DefaultStr = DefaultStr(0),
        bypass: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.63 deflicker
        Remove temporal frame luminance variations.

        It accepts the following options:

        Parameters:
        ----------

        :param int size: Set moving-average filter size in frames. Default is 5. Allowed range is 2 - 129.
        :param int mode: Set averaging mode to smooth temporal luminance variations. Available values are: ‘am’ Arithmetic mean ‘gm’ Geometric mean ‘hm’ Harmonic mean ‘qm’ Quadratic mean ‘cm’ Cubic mean ‘pm’ Power mean ‘median’ Median
        :param bool bypass: Do not actually modify frame. Useful when one only wants metadata.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#deflicker

        """
        filter_node = FilterNode(
            name="deflicker",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "size": size,
                "mode": mode,
                "bypass": bypass,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def dejudder(self, *, cycle: int | DefaultInt = DefaultInt(4), **kwargs: Any) -> "VideoStream":
        """

        11.64 dejudder
        Remove judder produced by partially interlaced telecined content.

        Judder can be introduced, for instance, by pullup filter. If the original
        source was partially telecined content then the output of pullup,dejudder
        will have a variable frame rate. May change the recorded frame rate of the
        container. Aside from that change, this filter will not affect constant frame
        rate video.

        The option available in this filter is:

        Parameters:
        ----------

        :param int cycle: Specify the length of the window over which the judder repeats. Accepts any integer greater than 1. Useful values are: ‘4’ If the original was telecined from 24 to 30 fps (Film to NTSC). ‘5’ If the original was telecined from 25 to 30 fps (PAL to NTSC). ‘20’ If a mixture of the two. The default is ‘4’.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#dejudder

        """
        filter_node = FilterNode(
            name="dejudder",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "cycle": cycle,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def delogo(
        self,
        *,
        x: str | DefaultStr = DefaultStr("-1"),
        y: str | DefaultStr = DefaultStr("-1"),
        w: str | DefaultStr = DefaultStr("-1"),
        h: str | DefaultStr = DefaultStr("-1"),
        show: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.65 delogo
        Suppress a TV station logo by a simple interpolation of the surrounding
        pixels. Just set a rectangle covering the logo and watch it disappear
        (and sometimes something even uglier appear - your mileage may vary).

        It accepts the following parameters:

        Parameters:
        ----------

        :param str x: Specify the top left corner coordinates of the logo. They must be specified.
        :param str y: Specify the top left corner coordinates of the logo. They must be specified.
        :param str w: Specify the width and height of the logo to clear. They must be specified.
        :param str h: Specify the width and height of the logo to clear. They must be specified.
        :param bool show: When set to 1, a green rectangle is drawn on the screen to simplify finding the right x, y, w, and h parameters. The default value is 0. The rectangle is drawn on the outermost pixels which will be (partly) replaced with interpolated values. The values of the next pixels immediately outside this rectangle in each direction will be used to compute the interpolated pixel values inside the rectangle.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#delogo

        """
        filter_node = FilterNode(
            name="delogo",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "show": show,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def derain(
        self,
        *,
        filter_type: int | Literal["derain", "dehaze"] | DefaultStr = DefaultStr("derain"),
        dnn_backend: int | DefaultInt = DefaultInt(1),
        model: str,
        input: str | DefaultStr = DefaultStr("x"),
        output: str | DefaultStr = DefaultStr("y"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.66 derain
        Remove the rain in the input image/video by applying the derain methods based on
        convolutional neural networks. Supported models:


         Recurrent Squeeze-and-Excitation Context Aggregation Net (RESCAN).
        See http://openaccess.thecvf.com/content_ECCV_2018/papers/Xia_Li_Recurrent_Squeeze-and-Excitation_Context_ECCV_2018_paper.pdf.

        Training as well as model generation scripts are provided in
        the repository at https://github.com/XueweiMeng/derain_filter.git.

        The filter accepts the following options:


        To get full functionality (such as async execution), please use the dnn_processing filter.

        Parameters:
        ----------

        :param int filter_type: Specify which filter to use. This option accepts the following values: ‘derain’ Derain filter. To conduct derain filter, you need to use a derain model. ‘dehaze’ Dehaze filter. To conduct dehaze filter, you need to use a dehaze model. Default value is ‘derain’.
        :param int dnn_backend: Specify which DNN backend to use for model loading and execution. This option accepts the following values: ‘tensorflow’ TensorFlow backend. To enable this backend you need to install the TensorFlow for C library (see https://www.tensorflow.org/install/lang_c) and configure FFmpeg with --enable-libtensorflow
        :param str model: Set path to model file specifying network architecture and its parameters. Note that different backends use different file formats. TensorFlow can load files for only its format.
        :param str input: None
        :param str output: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#derain

        """
        filter_node = FilterNode(
            name="derain",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "filter_type": filter_type,
                "dnn_backend": dnn_backend,
                "model": model,
                "input": input,
                "output": output,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def deshake(
        self,
        *,
        x: int | DefaultInt = DefaultInt(-1),
        y: int | DefaultInt = DefaultInt(-1),
        w: int | DefaultInt = DefaultInt(-1),
        h: int | DefaultInt = DefaultInt(-1),
        rx: int | DefaultInt = DefaultInt(16),
        ry: int | DefaultInt = DefaultInt(16),
        edge: int | Literal["blank", "original", "clamp", "mirror"] | DefaultStr = DefaultStr("mirror"),
        blocksize: int | DefaultInt = DefaultInt(8),
        contrast: int | DefaultInt = DefaultInt(125),
        search: int | Literal["exhaustive", "less"] | DefaultStr = DefaultStr("exhaustive"),
        filename: str,
        opencl: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.67 deshake
        Attempt to fix small changes in horizontal and/or vertical shift. This
        filter helps remove camera shake from hand-holding a camera, bumping a
        tripod, moving on a vehicle, etc.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int x: Specify a rectangular area where to limit the search for motion vectors. If desired the search for motion vectors can be limited to a rectangular area of the frame defined by its top left corner, width and height. These parameters have the same meaning as the drawbox filter which can be used to visualise the position of the bounding box. This is useful when simultaneous movement of subjects within the frame might be confused for camera motion by the motion vector search. If any or all of x, y, w and h are set to -1 then the full frame is used. This allows later options to be set without specifying the bounding box for the motion vector search. Default - search the whole frame.
        :param int y: Specify a rectangular area where to limit the search for motion vectors. If desired the search for motion vectors can be limited to a rectangular area of the frame defined by its top left corner, width and height. These parameters have the same meaning as the drawbox filter which can be used to visualise the position of the bounding box. This is useful when simultaneous movement of subjects within the frame might be confused for camera motion by the motion vector search. If any or all of x, y, w and h are set to -1 then the full frame is used. This allows later options to be set without specifying the bounding box for the motion vector search. Default - search the whole frame.
        :param int w: Specify a rectangular area where to limit the search for motion vectors. If desired the search for motion vectors can be limited to a rectangular area of the frame defined by its top left corner, width and height. These parameters have the same meaning as the drawbox filter which can be used to visualise the position of the bounding box. This is useful when simultaneous movement of subjects within the frame might be confused for camera motion by the motion vector search. If any or all of x, y, w and h are set to -1 then the full frame is used. This allows later options to be set without specifying the bounding box for the motion vector search. Default - search the whole frame.
        :param int h: Specify a rectangular area where to limit the search for motion vectors. If desired the search for motion vectors can be limited to a rectangular area of the frame defined by its top left corner, width and height. These parameters have the same meaning as the drawbox filter which can be used to visualise the position of the bounding box. This is useful when simultaneous movement of subjects within the frame might be confused for camera motion by the motion vector search. If any or all of x, y, w and h are set to -1 then the full frame is used. This allows later options to be set without specifying the bounding box for the motion vector search. Default - search the whole frame.
        :param int rx: Specify the maximum extent of movement in x and y directions in the range 0-64 pixels. Default 16.
        :param int ry: Specify the maximum extent of movement in x and y directions in the range 0-64 pixels. Default 16.
        :param int edge: Specify how to generate pixels to fill blanks at the edge of the frame. Available values are: ‘blank, 0’ Fill zeroes at blank locations ‘original, 1’ Original image at blank locations ‘clamp, 2’ Extruded edge value at blank locations ‘mirror, 3’ Mirrored edge at blank locations Default value is ‘mirror’.
        :param int blocksize: Specify the blocksize to use for motion search. Range 4-128 pixels, default 8.
        :param int contrast: Specify the contrast threshold for blocks. Only blocks with more than the specified contrast (difference between darkest and lightest pixels) will be considered. Range 1-255, default 125.
        :param int search: Specify the search strategy. Available values are: ‘exhaustive, 0’ Set exhaustive search ‘less, 1’ Set less exhaustive search. Default value is ‘exhaustive’.
        :param str filename: If set then a detailed log of the motion search is written to the specified file.
        :param bool opencl: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#deshake

        """
        filter_node = FilterNode(
            name="deshake",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "rx": rx,
                "ry": ry,
                "edge": edge,
                "blocksize": blocksize,
                "contrast": contrast,
                "search": search,
                "filename": filename,
                "opencl": opencl,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def deshake_opencl(
        self,
        *,
        tripod: bool | DefaultInt = DefaultInt(0),
        debug: bool | DefaultInt = DefaultInt(0),
        adaptive_crop: bool | DefaultInt = DefaultInt(1),
        refine_features: bool | DefaultInt = DefaultInt(1),
        smooth_strength: float | DefaultStr = DefaultStr("0.0f"),
        smooth_window_multiplier: float | DefaultFloat = DefaultFloat(2.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.6 deshake_opencl
        Feature-point based video stabilization filter.

        The filter accepts the following options:

        Parameters:
        ----------

        :param bool tripod: Simulates a tripod by preventing any camera movement whatsoever from the original frame. Defaults to 0.
        :param bool debug: Whether or not additional debug info should be displayed, both in the processed output and in the console. Note that in order to see console debug output you will also need to pass -v verbose to ffmpeg. Viewing point matches in the output video is only supported for RGB input. Defaults to 0.
        :param bool adaptive_crop: Whether or not to do a tiny bit of cropping at the borders to cut down on the amount of mirrored pixels. Defaults to 1.
        :param bool refine_features: Whether or not feature points should be refined at a sub-pixel level. This can be turned off for a slight performance gain at the cost of precision. Defaults to 1.
        :param float smooth_strength: The strength of the smoothing applied to the camera path from 0.0 to 1.0. 1.0 is the maximum smoothing strength while values less than that result in less smoothing. 0.0 causes the filter to adaptively choose a smoothing strength on a per-frame basis. Defaults to 0.0.
        :param float smooth_window_multiplier: Controls the size of the smoothing window (the number of frames buffered to determine motion information from). The size of the smoothing window is determined by multiplying the framerate of the video by this number. Acceptable values range from 0.1 to 10.0. Larger values increase the amount of motion data available for determining how to smooth the camera path, potentially improving smoothness, but also increase latency and memory usage. Defaults to 2.0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#deshake_005fopencl

        """
        filter_node = FilterNode(
            name="deshake_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "tripod": tripod,
                "debug": debug,
                "adaptive_crop": adaptive_crop,
                "refine_features": refine_features,
                "smooth_strength": smooth_strength,
                "smooth_window_multiplier": smooth_window_multiplier,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def despill(
        self,
        *,
        type: int | Literal["green", "blue"] | DefaultStr = DefaultStr("green"),
        mix: float | DefaultFloat = DefaultFloat(0.5),
        expand: float | DefaultFloat = DefaultFloat(0.0),
        red: float | DefaultFloat = DefaultFloat(0.0),
        green: float | DefaultFloat = DefaultFloat(-1.0),
        blue: float | DefaultFloat = DefaultFloat(0.0),
        brightness: float | DefaultFloat = DefaultFloat(0.0),
        alpha: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.68 despill
        Remove unwanted contamination of foreground colors, caused by reflected color of
        greenscreen or bluescreen.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int type: Set what type of despill to use.
        :param float mix: Set how spillmap will be generated.
        :param float expand: Set how much to get rid of still remaining spill.
        :param float red: Controls amount of red in spill area.
        :param float green: Controls amount of green in spill area. Should be -1 for greenscreen.
        :param float blue: Controls amount of blue in spill area. Should be -1 for bluescreen.
        :param float brightness: Controls brightness of spill area, preserving colors.
        :param bool alpha: Modify alpha from generated spillmap.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#despill

        """
        filter_node = FilterNode(
            name="despill",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "type": type,
                "mix": mix,
                "expand": expand,
                "red": red,
                "green": green,
                "blue": blue,
                "brightness": brightness,
                "alpha": alpha,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def detelecine(
        self,
        *,
        first_field: int | Literal["top", "t", "bottom", "b"] | DefaultStr = DefaultStr("top"),
        pattern: str | DefaultStr = DefaultStr("23"),
        start_frame: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.69 detelecine
        Apply an exact inverse of the telecine operation. It requires a predefined
        pattern specified using the pattern option which must be the same as that passed
        to the telecine filter.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int first_field: ‘top, t’ top field first ‘bottom, b’ bottom field first The default value is top.
        :param str pattern: A string of numbers representing the pulldown pattern you wish to apply. The default value is 23.
        :param int start_frame: A number representing position of the first frame with respect to the telecine pattern. This is to be used if the stream is cut. The default value is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#detelecine

        """
        filter_node = FilterNode(
            name="detelecine",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "first_field": first_field,
                "pattern": pattern,
                "start_frame": start_frame,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def dilation(
        self,
        *,
        coordinates: int | DefaultInt = DefaultInt(255),
        threshold0: int | DefaultInt = DefaultInt(65535),
        threshold1: int | DefaultInt = DefaultInt(65535),
        threshold2: int | DefaultInt = DefaultInt(65535),
        threshold3: int | DefaultInt = DefaultInt(65535),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.70 dilation
        Apply dilation effect to the video.

        This filter replaces the pixel by the local(3x3) maximum.

        It accepts the following options:

        Parameters:
        ----------

        :param int coordinates: Flag which specifies the pixel to refer to. Default is 255 i.e. all eight pixels are used. Flags to local 3x3 coordinates maps like this: 1 2 3 4 5 6 7 8
        :param int threshold0: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold1: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold2: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold3: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#dilation

        """
        filter_node = FilterNode(
            name="dilation",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "coordinates": coordinates,
                "threshold0": threshold0,
                "threshold1": threshold1,
                "threshold2": threshold2,
                "threshold3": threshold3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def dilation_opencl(
        self,
        *,
        threshold0: float | DefaultFloat = DefaultFloat(65535.0),
        threshold1: float | DefaultFloat = DefaultFloat(65535.0),
        threshold2: float | DefaultFloat = DefaultFloat(65535.0),
        threshold3: float | DefaultFloat = DefaultFloat(65535.0),
        coordinates: int | DefaultInt = DefaultInt(255),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.7 dilation_opencl
        Apply dilation effect to the video.

        This filter replaces the pixel by the local(3x3) maximum.

        It accepts the following options:

        Parameters:
        ----------

        :param float threshold0: Limit the maximum change for each plane. Range is [0, 65535] and default value is 65535. If 0, plane will remain unchanged.
        :param float threshold1: Limit the maximum change for each plane. Range is [0, 65535] and default value is 65535. If 0, plane will remain unchanged.
        :param float threshold2: Limit the maximum change for each plane. Range is [0, 65535] and default value is 65535. If 0, plane will remain unchanged.
        :param float threshold3: Limit the maximum change for each plane. Range is [0, 65535] and default value is 65535. If 0, plane will remain unchanged.
        :param int coordinates: Flag which specifies the pixel to refer to. Range is [0, 255] and default value is 255, i.e. all eight pixels are used. Flags to local 3x3 coordinates region centered on x: 1 2 3 4 x 5 6 7 8

        Ref: https://ffmpeg.org/ffmpeg-filters.html#dilation_005fopencl

        """
        filter_node = FilterNode(
            name="dilation_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "threshold0": threshold0,
                "threshold1": threshold1,
                "threshold2": threshold2,
                "threshold3": threshold3,
                "coordinates": coordinates,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def displace(
        self,
        _xmap: "VideoStream",
        _ymap: "VideoStream",
        *,
        edge: int | Literal["blank", "smear", "wrap", "mirror"] | DefaultStr = DefaultStr("smear"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.71 displace
        Displace pixels as indicated by second and third input stream.

        It takes three input streams and outputs one stream, the first input is the
        source, and second and third input are displacement maps.

        The second input specifies how much to displace pixels along the
        x-axis, while the third input specifies how much to displace pixels
        along the y-axis.
        If one of displacement map streams terminates, last frame from that
        displacement map will be used.

        Note that once generated, displacements maps can be reused over and over again.

        A description of the accepted options follows.

        Parameters:
        ----------

        :param int edge: Set displace behavior for pixels that are out of range. Available values are: ‘blank’ Missing pixels are replaced by black pixels. ‘smear’ Adjacent pixels will spread out to replace missing pixels. ‘wrap’ Out of range pixels are wrapped so they point to pixels of other side. ‘mirror’ Out of range pixels will be replaced with mirrored pixels. Default is ‘smear’.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#displace

        """
        filter_node = FilterNode(
            name="displace",
            input_typings=[StreamType.video, StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _xmap,
                _ymap,
            ],
            kwargs={
                "edge": edge,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def dnn_classify(
        self,
        *,
        dnn_backend: int | DefaultStr = DefaultStr("DNN_OV"),
        model: str,
        input: str,
        output: str,
        backend_configs: str,
        _async: bool | DefaultInt = DefaultInt(1),
        confidence: float | DefaultFloat = DefaultFloat(0.5),
        labels: str,
        target: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.72 dnn_classify
        Do classification with deep neural networks based on bounding boxes.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int dnn_backend: Specify which DNN backend to use for model loading and execution. This option accepts only openvino now, tensorflow backends will be added.
        :param str model: Set path to model file specifying network architecture and its parameters. Note that different backends use different file formats.
        :param str input: Set the input name of the dnn network.
        :param str output: Set the output name of the dnn network.
        :param str backend_configs: Set the configs to be passed into backend For tensorflow backend, you can set its configs with sess_config options, please use tools/python/tf_sess_config.py to get the configs for your system.
        :param bool _async: None
        :param float confidence: Set the confidence threshold (default: 0.5).
        :param str labels: Set path to label file specifying the mapping between label id and name. Each label name is written in one line, tailing spaces and empty lines are skipped. The first line is the name of label id 0, and the second line is the name of label id 1, etc. The label id is considered as name if the label file is not provided.
        :param str target: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#dnn_005fclassify

        """
        filter_node = FilterNode(
            name="dnn_classify",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dnn_backend": dnn_backend,
                "model": model,
                "input": input,
                "output": output,
                "backend_configs": backend_configs,
                "async": _async,
                "confidence": confidence,
                "labels": labels,
                "target": target,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def dnn_detect(
        self,
        *,
        dnn_backend: int | DefaultStr = DefaultStr("DNN_OV"),
        model: str,
        input: str,
        output: str,
        backend_configs: str,
        _async: bool | DefaultInt = DefaultInt(1),
        confidence: float | DefaultFloat = DefaultFloat(0.5),
        labels: str,
        model_type: int | Literal["ssd", "yolo", "yolov3", "yolov4"] | DefaultStr = DefaultStr("ssd"),
        cell_w: int | DefaultInt = DefaultInt(0),
        cell_h: int | DefaultInt = DefaultInt(0),
        nb_classes: int | DefaultInt = DefaultInt(0),
        anchors: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.73 dnn_detect
        Do object detection with deep neural networks.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int dnn_backend: Specify which DNN backend to use for model loading and execution. This option accepts only openvino now, tensorflow backends will be added.
        :param str model: Set path to model file specifying network architecture and its parameters. Note that different backends use different file formats.
        :param str input: Set the input name of the dnn network.
        :param str output: Set the output name of the dnn network.
        :param str backend_configs: Set the configs to be passed into backend. To use async execution, set async (default: set). Roll back to sync execution if the backend does not support async.
        :param bool _async: None
        :param float confidence: Set the confidence threshold (default: 0.5).
        :param str labels: Set path to label file specifying the mapping between label id and name. Each label name is written in one line, tailing spaces and empty lines are skipped. The first line is the name of label id 0 (usually it is ’background’), and the second line is the name of label id 1, etc. The label id is considered as name if the label file is not provided.
        :param int model_type: None
        :param int cell_w: None
        :param int cell_h: None
        :param int nb_classes: None
        :param str anchors: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#dnn_005fdetect

        """
        filter_node = FilterNode(
            name="dnn_detect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dnn_backend": dnn_backend,
                "model": model,
                "input": input,
                "output": output,
                "backend_configs": backend_configs,
                "async": _async,
                "confidence": confidence,
                "labels": labels,
                "model_type": model_type,
                "cell_w": cell_w,
                "cell_h": cell_h,
                "nb_classes": nb_classes,
                "anchors": anchors,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def dnn_processing(
        self,
        *,
        dnn_backend: int | DefaultStr = DefaultStr("DNN_TF"),
        model: str,
        input: str,
        output: str,
        backend_configs: str,
        _async: bool | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.74 dnn_processing
        Do image processing with deep neural networks. It works together with another filter
        which converts the pixel format of the Frame to what the dnn network requires.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int dnn_backend: Specify which DNN backend to use for model loading and execution. This option accepts the following values: ‘tensorflow’ TensorFlow backend. To enable this backend you need to install the TensorFlow for C library (see https://www.tensorflow.org/install/lang_c) and configure FFmpeg with --enable-libtensorflow ‘openvino’ OpenVINO backend. To enable this backend you need to build and install the OpenVINO for C library (see https://github.com/openvinotoolkit/openvino/blob/master/build-instruction.md) and configure FFmpeg with --enable-libopenvino (–extra-cflags=-I... –extra-ldflags=-L... might be needed if the header files and libraries are not installed into system path)
        :param str model: Set path to model file specifying network architecture and its parameters. Note that different backends use different file formats. TensorFlow, OpenVINO backend can load files for only its format.
        :param str input: Set the input name of the dnn network.
        :param str output: Set the output name of the dnn network.
        :param str backend_configs: Set the configs to be passed into backend. To use async execution, set async (default: set). Roll back to sync execution if the backend does not support async. For tensorflow backend, you can set its configs with sess_config options, please use tools/python/tf_sess_config.py to get the configs of TensorFlow backend for your system.
        :param bool _async: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#dnn_005fprocessing

        """
        filter_node = FilterNode(
            name="dnn_processing",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dnn_backend": dnn_backend,
                "model": model,
                "input": input,
                "output": output,
                "backend_configs": backend_configs,
                "async": _async,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def doubleweave(
        self, *, first_field: int | Literal["top", "t", "bottom", "b"] | DefaultStr = DefaultStr("top"), **kwargs: Any
    ) -> "VideoStream":
        """

        11.285 weave, doubleweave
        The weave takes a field-based video input and join
        each two sequential fields into single frame, producing a new double
        height clip with half the frame rate and half the frame count.

        The doubleweave works same as weave but without
        halving frame rate and frame count.

        It accepts the following option:

        Parameters:
        ----------

        :param int first_field: Set first field. Available values are: ‘top, t’ Set the frame as top-field-first. ‘bottom, b’ Set the frame as bottom-field-first.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#weave_002c-doubleweave

        """
        filter_node = FilterNode(
            name="doubleweave",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "first_field": first_field,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def drawbox(
        self,
        *,
        x: str | DefaultStr = DefaultStr("0"),
        y: str | DefaultStr = DefaultStr("0"),
        width: str | DefaultStr = DefaultStr("0"),
        height: str | DefaultStr = DefaultStr("0"),
        color: str | DefaultStr = DefaultStr("black"),
        thickness: str | DefaultStr = DefaultStr("3"),
        replace: bool | DefaultInt = DefaultInt(0),
        box_source: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.75 drawbox
        Draw a colored box on the input image.

        It accepts the following parameters:


        The parameters for x, y, w and h and t are expressions containing the
        following constants:

        Parameters:
        ----------

        :param str x: The expressions which specify the top left corner coordinates of the box. It defaults to 0.
        :param str y: The expressions which specify the top left corner coordinates of the box. It defaults to 0.
        :param str width: The expressions which specify the width and height of the box; if 0 they are interpreted as the input width and height. It defaults to 0.
        :param str height: The expressions which specify the width and height of the box; if 0 they are interpreted as the input width and height. It defaults to 0.
        :param str color: Specify the color of the box to write. For the general syntax of this option, check the (ffmpeg-utils)"Color" section in the ffmpeg-utils manual. If the special value invert is used, the box edge color is the same as the video with inverted luma.
        :param str thickness: The expression which sets the thickness of the box edge. A value of fill will create a filled box. Default value is 3. See below for the list of accepted constants.
        :param bool replace: Applicable if the input has alpha. With value 1, the pixels of the painted box will overwrite the video’s color and alpha pixels. Default is 0, which composites the box onto the input, leaving the video’s alpha intact.
        :param str box_source: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#drawbox

        """
        filter_node = FilterNode(
            name="drawbox",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "color": color,
                "thickness": thickness,
                "replace": replace,
                "box_source": box_source,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def drawgraph(
        self,
        *,
        m1: str | DefaultStr = DefaultStr(""),
        fg1: str | DefaultStr = DefaultStr("0xffff0000"),
        m2: str | DefaultStr = DefaultStr(""),
        fg2: str | DefaultStr = DefaultStr("0xff00ff00"),
        m3: str | DefaultStr = DefaultStr(""),
        fg3: str | DefaultStr = DefaultStr("0xffff00ff"),
        m4: str | DefaultStr = DefaultStr(""),
        fg4: str | DefaultStr = DefaultStr("0xffffff00"),
        bg: str | DefaultStr = DefaultStr("white"),
        min: float | DefaultFloat = DefaultFloat(-1.0),
        max: float | DefaultFloat = DefaultFloat(1.0),
        mode: int | Literal["bar", "dot", "line"] | DefaultStr = DefaultStr("line"),
        slide: int | Literal["frame", "replace", "scroll", "rscroll", "picture"] | DefaultStr = DefaultStr("frame"),
        size: str | DefaultStr = DefaultStr("900x256"),
        rate: str | DefaultStr = DefaultStr("25"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.76 drawgraph
        Draw a graph using input video metadata.

        It accepts the following parameters:


        Example using metadata from signalstats filter:

        signalstats,drawgraph=lavfi.signalstats.YAVG:min=0:max=255

        Example using metadata from ebur128 filter:

        ebur128=metadata=1,adrawgraph=lavfi.r128.M:min=-120:max=5

        Parameters:
        ----------

        :param str m1: Set 1st frame metadata key from which metadata values will be used to draw a graph.
        :param str fg1: Set 1st foreground color expression.
        :param str m2: Set 2nd frame metadata key from which metadata values will be used to draw a graph.
        :param str fg2: Set 2nd foreground color expression.
        :param str m3: Set 3rd frame metadata key from which metadata values will be used to draw a graph.
        :param str fg3: Set 3rd foreground color expression.
        :param str m4: Set 4th frame metadata key from which metadata values will be used to draw a graph.
        :param str fg4: Set 4th foreground color expression.
        :param str bg: Set graph background color. Default is white.
        :param float min: Set minimal value of metadata value.
        :param float max: Set maximal value of metadata value.
        :param int mode: Set graph mode. Available values for mode is: ‘bar’ ‘dot’ ‘line’ Default is line.
        :param int slide: Set slide mode. Available values for slide is: ‘frame’ Draw new frame when right border is reached. ‘replace’ Replace old columns with new ones. ‘scroll’ Scroll from right to left. ‘rscroll’ Scroll from left to right. ‘picture’ Draw single picture. Default is frame.
        :param str size: Set size of graph video. For the syntax of this option, check the (ffmpeg-utils)"Video size" section in the ffmpeg-utils manual. The default value is 900x256.
        :param str rate: Set the output frame rate. Default value is 25. The foreground color expressions can use the following variables: MIN Minimal value of metadata value. MAX Maximal value of metadata value. VAL Current metadata key value. The color is defined as 0xAABBGGRR.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#drawgraph

        """
        filter_node = FilterNode(
            name="drawgraph",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "m1": m1,
                "fg1": fg1,
                "m2": m2,
                "fg2": fg2,
                "m3": m3,
                "fg3": fg3,
                "m4": m4,
                "fg4": fg4,
                "bg": bg,
                "min": min,
                "max": max,
                "mode": mode,
                "slide": slide,
                "size": size,
                "rate": rate,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def drawgrid(
        self,
        *,
        x: str | DefaultStr = DefaultStr("0"),
        y: str | DefaultStr = DefaultStr("0"),
        width: str | DefaultStr = DefaultStr("0"),
        height: str | DefaultStr = DefaultStr("0"),
        color: str | DefaultStr = DefaultStr("black"),
        thickness: str | DefaultStr = DefaultStr("1"),
        replace: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.77 drawgrid
        Draw a grid on the input image.

        It accepts the following parameters:


        The parameters for x, y, w and h and t are expressions containing the
        following constants:

        Parameters:
        ----------

        :param str x: The expressions which specify the coordinates of some point of grid intersection (meant to configure offset). Both default to 0.
        :param str y: The expressions which specify the coordinates of some point of grid intersection (meant to configure offset). Both default to 0.
        :param str width: The expressions which specify the width and height of the grid cell, if 0 they are interpreted as the input width and height, respectively, minus thickness, so image gets framed. Default to 0.
        :param str height: The expressions which specify the width and height of the grid cell, if 0 they are interpreted as the input width and height, respectively, minus thickness, so image gets framed. Default to 0.
        :param str color: Specify the color of the grid. For the general syntax of this option, check the (ffmpeg-utils)"Color" section in the ffmpeg-utils manual. If the special value invert is used, the grid color is the same as the video with inverted luma.
        :param str thickness: The expression which sets the thickness of the grid line. Default value is 1. See below for the list of accepted constants.
        :param bool replace: Applicable if the input has alpha. With 1 the pixels of the painted grid will overwrite the video’s color and alpha pixels. Default is 0, which composites the grid onto the input, leaving the video’s alpha intact.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#drawgrid

        """
        filter_node = FilterNode(
            name="drawgrid",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "color": color,
                "thickness": thickness,
                "replace": replace,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def drawtext(
        self,
        *,
        fontfile: str,
        text: str,
        textfile: str,
        fontcolor: str | DefaultStr = DefaultStr("black"),
        fontcolor_expr: str | DefaultStr = DefaultStr(""),
        boxcolor: str | DefaultStr = DefaultStr("white"),
        bordercolor: str | DefaultStr = DefaultStr("black"),
        shadowcolor: str | DefaultStr = DefaultStr("black"),
        box: bool | DefaultInt = DefaultInt(0),
        boxborderw: str | DefaultStr = DefaultStr("0"),
        line_spacing: int | DefaultInt = DefaultInt(0),
        fontsize: str,
        text_align: str | DefaultStr = DefaultStr(0),
        x: str | DefaultStr = DefaultStr("0"),
        y: str | DefaultStr = DefaultStr("0"),
        boxw: int | DefaultInt = DefaultInt(0),
        boxh: int | DefaultInt = DefaultInt(0),
        shadowx: int | DefaultInt = DefaultInt(0),
        shadowy: int | DefaultInt = DefaultInt(0),
        borderw: int | DefaultInt = DefaultInt(0),
        tabsize: int | DefaultInt = DefaultInt(4),
        basetime: int | DefaultStr = DefaultStr("((int64_t)(0x8000000000000000ULL))"),
        expansion: int | Literal["none", "normal", "strftime"] | DefaultStr = DefaultStr("normal"),
        y_align: int | Literal["text", "baseline", "font"] | DefaultStr = DefaultStr("text"),
        timecode: str,
        tc24hmax: bool | DefaultInt = DefaultInt(0),
        timecode_rate: float | DefaultFloat = DefaultFloat(0.0),
        reload: int | DefaultInt = DefaultInt(0),
        alpha: str | DefaultStr = DefaultStr("1"),
        fix_bounds: bool | DefaultInt = DefaultInt(0),
        start_number: int | DefaultInt = DefaultInt(0),
        text_source: str,
        ft_load_flags: str | DefaultStr = DefaultStr("FT_LOAD_DEFAULT"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.78 drawtext
        Draw a text string or text from a specified file on top of a video, using the
        libfreetype library.

        To enable compilation of this filter, you need to configure FFmpeg with
        --enable-libfreetype and --enable-libharfbuzz.
        To enable default font fallback and the font option you need to
        configure FFmpeg with --enable-libfontconfig.
        To enable the text_shaping option, you need to configure FFmpeg with
        --enable-libfribidi.

        Parameters:
        ----------

        :param str fontfile: None
        :param str text: None
        :param str textfile: None
        :param str fontcolor: None
        :param str fontcolor_expr: None
        :param str boxcolor: None
        :param str bordercolor: None
        :param str shadowcolor: None
        :param bool box: None
        :param str boxborderw: None
        :param int line_spacing: None
        :param str fontsize: None
        :param str text_align: None
        :param str x: None
        :param str y: None
        :param int boxw: None
        :param int boxh: None
        :param int shadowx: None
        :param int shadowy: None
        :param int borderw: None
        :param int tabsize: None
        :param int basetime: None
        :param int expansion: None
        :param int y_align: None
        :param str timecode: None
        :param bool tc24hmax: None
        :param float timecode_rate: None
        :param int reload: None
        :param str alpha: None
        :param bool fix_bounds: None
        :param int start_number: None
        :param str text_source: None
        :param str ft_load_flags: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#drawtext

        """
        filter_node = FilterNode(
            name="drawtext",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "fontfile": fontfile,
                "text": text,
                "textfile": textfile,
                "fontcolor": fontcolor,
                "fontcolor_expr": fontcolor_expr,
                "boxcolor": boxcolor,
                "bordercolor": bordercolor,
                "shadowcolor": shadowcolor,
                "box": box,
                "boxborderw": boxborderw,
                "line_spacing": line_spacing,
                "fontsize": fontsize,
                "text_align": text_align,
                "x": x,
                "y": y,
                "boxw": boxw,
                "boxh": boxh,
                "shadowx": shadowx,
                "shadowy": shadowy,
                "borderw": borderw,
                "tabsize": tabsize,
                "basetime": basetime,
                "expansion": expansion,
                "y_align": y_align,
                "timecode": timecode,
                "tc24hmax": tc24hmax,
                "timecode_rate": timecode_rate,
                "reload": reload,
                "alpha": alpha,
                "fix_bounds": fix_bounds,
                "start_number": start_number,
                "text_source": text_source,
                "ft_load_flags": ft_load_flags,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def edgedetect(
        self,
        *,
        high: float | DefaultStr = DefaultStr("50/255."),
        low: float | DefaultStr = DefaultStr("20/255."),
        mode: int | Literal["wires", "colormix", "canny"] | DefaultStr = DefaultStr("wires"),
        planes: str | Literal["y", "u", "v", "r", "g", "b"] | DefaultStr = DefaultStr(7),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.79 edgedetect
        Detect and draw edges. The filter uses the Canny Edge Detection algorithm.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float high: Set low and high threshold values used by the Canny thresholding algorithm. The high threshold selects the "strong" edge pixels, which are then connected through 8-connectivity with the "weak" edge pixels selected by the low threshold. low and high threshold values must be chosen in the range [0,1], and low should be lesser or equal to high. Default value for low is 20/255, and default value for high is 50/255.
        :param float low: Set low and high threshold values used by the Canny thresholding algorithm. The high threshold selects the "strong" edge pixels, which are then connected through 8-connectivity with the "weak" edge pixels selected by the low threshold. low and high threshold values must be chosen in the range [0,1], and low should be lesser or equal to high. Default value for low is 20/255, and default value for high is 50/255.
        :param int mode: Define the drawing mode. ‘wires’ Draw white/gray wires on black background. ‘colormix’ Mix the colors to create a paint/cartoon effect. ‘canny’ Apply Canny edge detector on all selected planes. Default value is wires.
        :param str planes: Select planes for filtering. By default all available planes are filtered.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#edgedetect

        """
        filter_node = FilterNode(
            name="edgedetect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "high": high,
                "low": low,
                "mode": mode,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def elbg(
        self,
        *,
        codebook_length: int | DefaultInt = DefaultInt(256),
        nb_steps: int | DefaultInt = DefaultInt(1),
        seed: int | DefaultInt = DefaultInt(-1),
        pal8: bool | DefaultInt = DefaultInt(0),
        use_alpha: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.80 elbg
        Apply a posterize effect using the ELBG (Enhanced LBG) algorithm.

        For each input image, the filter will compute the optimal mapping from
        the input to the output given the codebook length, that is the number
        of distinct output colors.

        This filter accepts the following options.

        Parameters:
        ----------

        :param int codebook_length: Set codebook length. The value must be a positive integer, and represents the number of distinct output colors. Default value is 256.
        :param int nb_steps: Set the maximum number of iterations to apply for computing the optimal mapping. The higher the value the better the result and the higher the computation time. Default value is 1.
        :param int seed: Set a random seed, must be an integer included between 0 and UINT32_MAX. If not specified, or if explicitly set to -1, the filter will try to use a good random seed on a best effort basis.
        :param bool pal8: Set pal8 output pixel format. This option does not work with codebook length greater than 256. Default is disabled.
        :param bool use_alpha: Include alpha values in the quantization calculation. Allows creating palettized output images (e.g. PNG8) with multiple alpha smooth blending.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#elbg

        """
        filter_node = FilterNode(
            name="elbg",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "codebook_length": codebook_length,
                "nb_steps": nb_steps,
                "seed": seed,
                "pal8": pal8,
                "use_alpha": use_alpha,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def entropy(
        self, *, mode: int | Literal["normal", "diff"] | DefaultStr = DefaultStr("normal"), **kwargs: Any
    ) -> "VideoStream":
        """

        11.81 entropy
        Measure graylevel entropy in histogram of color channels of video frames.

        It accepts the following parameters:

        Parameters:
        ----------

        :param int mode: Can be either normal or diff. Default is normal. diff mode measures entropy of histogram delta values, absolute differences between neighbour histogram values.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#entropy

        """
        filter_node = FilterNode(
            name="entropy",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def epx(self, *, n: int | DefaultInt = DefaultInt(3), **kwargs: Any) -> "VideoStream":
        """

        11.82 epx
        Apply the EPX magnification filter which is designed for pixel art.

        It accepts the following option:

        Parameters:
        ----------

        :param int n: Set the scaling dimension: 2 for 2xEPX, 3 for 3xEPX. Default is 3.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#epx

        """
        filter_node = FilterNode(
            name="epx",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "n": n,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def eq(
        self,
        *,
        contrast: str | DefaultStr = DefaultStr("1.0"),
        brightness: str | DefaultStr = DefaultStr("0.0"),
        saturation: str | DefaultStr = DefaultStr("1.0"),
        gamma: str | DefaultStr = DefaultStr("1.0"),
        gamma_r: str | DefaultStr = DefaultStr("1.0"),
        gamma_g: str | DefaultStr = DefaultStr("1.0"),
        gamma_b: str | DefaultStr = DefaultStr("1.0"),
        gamma_weight: str | DefaultStr = DefaultStr("1.0"),
        eval: int | DefaultStr = DefaultStr("EVAL_MODE_INIT"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.83 eq
        Set brightness, contrast, saturation and approximate gamma adjustment.

        The filter accepts the following options:


        The expressions accept the following parameters:

        Parameters:
        ----------

        :param str contrast: Set the contrast expression. The value must be a float value in range -1000.0 to 1000.0. The default value is "1".
        :param str brightness: Set the brightness expression. The value must be a float value in range -1.0 to 1.0. The default value is "0".
        :param str saturation: Set the saturation expression. The value must be a float in range 0.0 to 3.0. The default value is "1".
        :param str gamma: Set the gamma expression. The value must be a float in range 0.1 to 10.0. The default value is "1".
        :param str gamma_r: Set the gamma expression for red. The value must be a float in range 0.1 to 10.0. The default value is "1".
        :param str gamma_g: Set the gamma expression for green. The value must be a float in range 0.1 to 10.0. The default value is "1".
        :param str gamma_b: Set the gamma expression for blue. The value must be a float in range 0.1 to 10.0. The default value is "1".
        :param str gamma_weight: Set the gamma weight expression. It can be used to reduce the effect of a high gamma value on bright image areas, e.g. keep them from getting overamplified and just plain white. The value must be a float in range 0.0 to 1.0. A value of 0.0 turns the gamma correction all the way down while 1.0 leaves it at its full strength. Default is "1".
        :param int eval: Set when the expressions for brightness, contrast, saturation and gamma expressions are evaluated. It accepts the following values: ‘init’ only evaluate expressions once during the filter initialization or when a command is processed ‘frame’ evaluate expressions for each incoming frame Default value is ‘init’.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#eq

        """
        filter_node = FilterNode(
            name="eq",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "contrast": contrast,
                "brightness": brightness,
                "saturation": saturation,
                "gamma": gamma,
                "gamma_r": gamma_r,
                "gamma_g": gamma_g,
                "gamma_b": gamma_b,
                "gamma_weight": gamma_weight,
                "eval": eval,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def erosion(
        self,
        *,
        coordinates: int | DefaultInt = DefaultInt(255),
        threshold0: int | DefaultInt = DefaultInt(65535),
        threshold1: int | DefaultInt = DefaultInt(65535),
        threshold2: int | DefaultInt = DefaultInt(65535),
        threshold3: int | DefaultInt = DefaultInt(65535),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.84 erosion
        Apply erosion effect to the video.

        This filter replaces the pixel by the local(3x3) minimum.

        It accepts the following options:

        Parameters:
        ----------

        :param int coordinates: Flag which specifies the pixel to refer to. Default is 255 i.e. all eight pixels are used. Flags to local 3x3 coordinates maps like this: 1 2 3 4 5 6 7 8
        :param int threshold0: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold1: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold2: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold3: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#erosion

        """
        filter_node = FilterNode(
            name="erosion",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "coordinates": coordinates,
                "threshold0": threshold0,
                "threshold1": threshold1,
                "threshold2": threshold2,
                "threshold3": threshold3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def erosion_opencl(
        self,
        *,
        threshold0: float | DefaultFloat = DefaultFloat(65535.0),
        threshold1: float | DefaultFloat = DefaultFloat(65535.0),
        threshold2: float | DefaultFloat = DefaultFloat(65535.0),
        threshold3: float | DefaultFloat = DefaultFloat(65535.0),
        coordinates: int | DefaultInt = DefaultInt(255),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.5 erosion_opencl
        Apply erosion effect to the video.

        This filter replaces the pixel by the local(3x3) minimum.

        It accepts the following options:

        Parameters:
        ----------

        :param float threshold0: Limit the maximum change for each plane. Range is [0, 65535] and default value is 65535. If 0, plane will remain unchanged.
        :param float threshold1: Limit the maximum change for each plane. Range is [0, 65535] and default value is 65535. If 0, plane will remain unchanged.
        :param float threshold2: Limit the maximum change for each plane. Range is [0, 65535] and default value is 65535. If 0, plane will remain unchanged.
        :param float threshold3: Limit the maximum change for each plane. Range is [0, 65535] and default value is 65535. If 0, plane will remain unchanged.
        :param int coordinates: Flag which specifies the pixel to refer to. Range is [0, 255] and default value is 255, i.e. all eight pixels are used. Flags to local 3x3 coordinates region centered on x: 1 2 3 4 x 5 6 7 8

        Ref: https://ffmpeg.org/ffmpeg-filters.html#erosion_005fopencl

        """
        filter_node = FilterNode(
            name="erosion_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "threshold0": threshold0,
                "threshold1": threshold1,
                "threshold2": threshold2,
                "threshold3": threshold3,
                "coordinates": coordinates,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def estdif(
        self,
        *,
        mode: int | Literal["frame", "field"] | DefaultStr = DefaultStr("field"),
        parity: int | Literal["tff", "bff", "auto"] | DefaultStr = DefaultStr("auto"),
        deint: int | Literal["all", "interlaced"] | DefaultStr = DefaultStr("all"),
        rslope: int | DefaultInt = DefaultInt(1),
        redge: int | DefaultInt = DefaultInt(2),
        ecost: int | DefaultInt = DefaultInt(2),
        mcost: int | DefaultInt = DefaultInt(1),
        dcost: int | DefaultInt = DefaultInt(1),
        interp: int | Literal["2p", "4p", "6p"] | DefaultStr = DefaultStr("4p"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.85 estdif
        Deinterlace the input video ("estdif" stands for "Edge Slope
        Tracing Deinterlacing Filter").

        Spatial only filter that uses edge slope tracing algorithm
        to interpolate missing lines.
        It accepts the following parameters:

        Parameters:
        ----------

        :param int mode: The interlacing mode to adopt. It accepts one of the following values: frame Output one frame for each frame. field Output one frame for each field. The default value is field.
        :param int parity: The picture field parity assumed for the input interlaced video. It accepts one of the following values: tff Assume the top field is first. bff Assume the bottom field is first. auto Enable automatic detection of field parity. The default value is auto. If the interlacing is unknown or the decoder does not export this information, top field first will be assumed.
        :param int deint: Specify which frames to deinterlace. Accepts one of the following values: all Deinterlace all frames. interlaced Only deinterlace frames marked as interlaced. The default value is all.
        :param int rslope: Specify the search radius for edge slope tracing. Default value is 1. Allowed range is from 1 to 15.
        :param int redge: Specify the search radius for best edge matching. Default value is 2. Allowed range is from 0 to 15.
        :param int ecost: Specify the edge cost for edge matching. Default value is 2. Allowed range is from 0 to 50.
        :param int mcost: Specify the middle cost for edge matching. Default value is 1. Allowed range is from 0 to 50.
        :param int dcost: Specify the distance cost for edge matching. Default value is 1. Allowed range is from 0 to 50.
        :param int interp: Specify the interpolation used. Default is 4-point interpolation. It accepts one of the following values: 2p Two-point interpolation. 4p Four-point interpolation. 6p Six-point interpolation.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#estdif

        """
        filter_node = FilterNode(
            name="estdif",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "parity": parity,
                "deint": deint,
                "rslope": rslope,
                "redge": redge,
                "ecost": ecost,
                "mcost": mcost,
                "dcost": dcost,
                "interp": interp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def exposure(
        self,
        *,
        exposure: float | DefaultFloat = DefaultFloat(0.0),
        black: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.86 exposure
        Adjust exposure of the video stream.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float exposure: Set the exposure correction in EV. Allowed range is from -3.0 to 3.0 EV Default value is 0 EV.
        :param float black: Set the black level correction. Allowed range is from -1.0 to 1.0. Default value is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#exposure

        """
        filter_node = FilterNode(
            name="exposure",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "exposure": exposure,
                "black": black,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def extractplanes(
        self, *, planes: str | Literal["y", "u", "v", "r", "g", "b", "a"] | DefaultStr = DefaultStr(1), **kwargs: Any
    ) -> FilterNode:
        """

        11.87 extractplanes
        Extract color channel components from input video stream into
        separate grayscale video streams.

        The filter accepts the following option:

        Parameters:
        ----------

        :param str planes: Set plane(s) to extract. Available values for planes are: ‘y’ ‘u’ ‘v’ ‘a’ ‘r’ ‘g’ ‘b’ Choosing planes not available in the input will result in an error. That means you cannot select r, g, b planes with y, u, v planes at same time.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#extractplanes

        """
        filter_node = FilterNode(
            name="extractplanes",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video] * len(planes.split("+")),
            inputs=[
                self,
            ],
            kwargs={
                "planes": planes,
            }
            | kwargs,
        )

        return filter_node

    def fade(
        self,
        *,
        type: int | DefaultInt = DefaultInt(0),
        start_frame: int | DefaultInt = DefaultInt(0),
        nb_frames: int | DefaultInt = DefaultInt(25),
        alpha: bool | DefaultInt = DefaultInt(0),
        start_time: int | DefaultStr = DefaultStr("0."),
        duration: int | DefaultStr = DefaultStr("0."),
        color: str | DefaultStr = DefaultStr("black"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.88 fade
        Apply a fade-in/out effect to the input video.

        It accepts the following parameters:

        Parameters:
        ----------

        :param int type: The effect type can be either "in" for a fade-in, or "out" for a fade-out effect. Default is in.
        :param int start_frame: Specify the number of the frame to start applying the fade effect at. Default is 0.
        :param int nb_frames: The number of frames that the fade effect lasts. At the end of the fade-in effect, the output video will have the same intensity as the input video. At the end of the fade-out transition, the output video will be filled with the selected color. Default is 25.
        :param bool alpha: If set to 1, fade only alpha channel, if one exists on the input. Default value is 0.
        :param int start_time: Specify the timestamp (in seconds) of the frame to start to apply the fade effect. If both start_frame and start_time are specified, the fade will start at whichever comes last. Default is 0.
        :param int duration: The number of seconds for which the fade effect has to last. At the end of the fade-in effect the output video will have the same intensity as the input video, at the end of the fade-out transition the output video will be filled with the selected color. If both duration and nb_frames are specified, duration is used. Default is 0 (nb_frames is used by default).
        :param str color: Specify the color of the fade. Default is "black".

        Ref: https://ffmpeg.org/ffmpeg-filters.html#fade

        """
        filter_node = FilterNode(
            name="fade",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "type": type,
                "start_frame": start_frame,
                "nb_frames": nb_frames,
                "alpha": alpha,
                "start_time": start_time,
                "duration": duration,
                "color": color,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def feedback(
        self,
        _feedin: "VideoStream",
        *,
        x: int | DefaultInt = DefaultInt(0),
        y: int | DefaultInt = DefaultInt(0),
        w: int | DefaultInt = DefaultInt(0),
        h: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> tuple["VideoStream", "VideoStream",]:
        """

        11.89 feedback
        Apply feedback video filter.

        This filter pass cropped input frames to 2nd output.
        From there it can be filtered with other video filters.
        After filter receives frame from 2nd input, that frame
        is combined on top of original frame from 1st input and passed
        to 1st output.

        The typical usage is filter only part of frame.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int x: Set the top left crop position.
        :param int y: Set the top left crop position.
        :param int w: Set the crop size.
        :param int h: Set the crop size.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#feedback

        """
        filter_node = FilterNode(
            name="feedback",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video, StreamType.video],
            inputs=[
                self,
                _feedin,
            ],
            kwargs={
                "x": x,
                "y": y,
                "w": w,
                "h": h,
            }
            | kwargs,
        )
        return (
            filter_node.video(0),
            filter_node.video(1),
        )

    def fftdnoiz(
        self,
        *,
        sigma: float | DefaultFloat = DefaultFloat(1.0),
        amount: float | DefaultFloat = DefaultFloat(1.0),
        block: int | DefaultInt = DefaultInt(32),
        overlap: float | DefaultFloat = DefaultFloat(0.5),
        method: int | Literal["wiener", "hard"] | DefaultStr = DefaultStr("wiener"),
        prev: int | DefaultInt = DefaultInt(0),
        next: int | DefaultInt = DefaultInt(0),
        planes: int | DefaultInt = DefaultInt(7),
        window: int
        | Literal[
            "rect",
            "bartlett",
            "hann",
            "hanning",
            "hamming",
            "blackman",
            "welch",
            "flattop",
            "bharris",
            "bnuttall",
            "bhann",
            "sine",
            "nuttall",
            "lanczos",
            "gauss",
            "tukey",
            "dolph",
            "cauchy",
            "parzen",
            "poisson",
            "bohman",
            "kaiser",
        ]
        | DefaultStr = DefaultStr("hann"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.90 fftdnoiz
        Denoise frames using 3D FFT (frequency domain filtering).

        The filter accepts the following options:

        Parameters:
        ----------

        :param float sigma: Set the noise sigma constant. This sets denoising strength. Default value is 1. Allowed range is from 0 to 30. Using very high sigma with low overlap may give blocking artifacts.
        :param float amount: Set amount of denoising. By default all detected noise is reduced. Default value is 1. Allowed range is from 0 to 1.
        :param int block: Set size of block in pixels, Default is 32, can be 8 to 256.
        :param float overlap: Set block overlap. Default is 0.5. Allowed range is from 0.2 to 0.8.
        :param int method: Set denoising method. Default is wiener, can also be hard.
        :param int prev: Set number of previous frames to use for denoising. By default is set to 0.
        :param int next: Set number of next frames to to use for denoising. By default is set to 0.
        :param int planes: Set planes which will be filtered, by default are all available filtered except alpha.
        :param int window: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#fftdnoiz

        """
        filter_node = FilterNode(
            name="fftdnoiz",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "sigma": sigma,
                "amount": amount,
                "block": block,
                "overlap": overlap,
                "method": method,
                "prev": prev,
                "next": next,
                "planes": planes,
                "window": window,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def fftfilt(
        self,
        *,
        dc_Y: int | DefaultInt = DefaultInt(0),
        dc_U: int | DefaultInt = DefaultInt(0),
        dc_V: int | DefaultInt = DefaultInt(0),
        weight_Y: str | DefaultStr = DefaultStr("1"),
        weight_U: str,
        weight_V: str,
        eval: int | DefaultStr = DefaultStr("EVAL_MODE_INIT"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.91 fftfilt
        Apply arbitrary expressions to samples in frequency domain

        Parameters:
        ----------

        :param int dc_Y: Adjust the dc value (gain) of the luma plane of the image. The filter accepts an integer value in range 0 to 1000. The default value is set to 0.
        :param int dc_U: Adjust the dc value (gain) of the 1st chroma plane of the image. The filter accepts an integer value in range 0 to 1000. The default value is set to 0.
        :param int dc_V: Adjust the dc value (gain) of the 2nd chroma plane of the image. The filter accepts an integer value in range 0 to 1000. The default value is set to 0.
        :param str weight_Y: Set the frequency domain weight expression for the luma plane.
        :param str weight_U: Set the frequency domain weight expression for the 1st chroma plane.
        :param str weight_V: Set the frequency domain weight expression for the 2nd chroma plane.
        :param int eval: Set when the expressions are evaluated. It accepts the following values: ‘init’ Only evaluate expressions once during the filter initialization. ‘frame’ Evaluate expressions for each incoming frame. Default value is ‘init’. The filter accepts the following variables:

        Ref: https://ffmpeg.org/ffmpeg-filters.html#fftfilt

        """
        filter_node = FilterNode(
            name="fftfilt",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dc_Y": dc_Y,
                "dc_U": dc_U,
                "dc_V": dc_V,
                "weight_Y": weight_Y,
                "weight_U": weight_U,
                "weight_V": weight_V,
                "eval": eval,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def field(
        self, *, type: int | Literal["top", "bottom"] | DefaultStr = DefaultStr("top"), **kwargs: Any
    ) -> "VideoStream":
        """

        11.92 field
        Extract a single field from an interlaced image using stride
        arithmetic to avoid wasting CPU time. The output frames are marked as
        non-interlaced.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int type: Specify whether to extract the top (if the value is 0 or top) or the bottom field (if the value is 1 or bottom).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#field

        """
        filter_node = FilterNode(
            name="field",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "type": type,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def fieldhint(
        self,
        *,
        hint: str,
        mode: int | Literal["absolute", "relative", "pattern"] | DefaultStr = DefaultStr(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.93 fieldhint
        Create new frames by copying the top and bottom fields from surrounding frames
        supplied as numbers by the hint file.


        Example of first several lines of hint file for relative mode:

        0,0 - # first frame
        1,0 - # second frame, use third's frame top field and second's frame bottom field
        1,0 - # third frame, use fourth's frame top field and third's frame bottom field
        1,0 -
        0,0 -
        0,0 -
        1,0 -
        1,0 -
        1,0 -
        0,0 -
        0,0 -
        1,0 -
        1,0 -
        1,0 -
        0,0 -

        Parameters:
        ----------

        :param str hint: Set file containing hints: absolute/relative frame numbers. There must be one line for each frame in a clip. Each line must contain two numbers separated by the comma, optionally followed by - or +. Numbers supplied on each line of file can not be out of [N-1,N+1] where N is current frame number for absolute mode or out of [-1, 1] range for relative mode. First number tells from which frame to pick up top field and second number tells from which frame to pick up bottom field. If optionally followed by + output frame will be marked as interlaced, else if followed by - output frame will be marked as progressive, else it will be marked same as input frame. If optionally followed by t output frame will use only top field, or in case of b it will use only bottom field. If line starts with # or ; that line is skipped.
        :param int mode: Can be item absolute or relative or pattern. Default is absolute. The pattern mode is same as relative mode, except at last entry of file if there are more frames to process than hint file is seek back to start.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#fieldhint

        """
        filter_node = FilterNode(
            name="fieldhint",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "hint": hint,
                "mode": mode,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def fieldorder(self, *, order: int | DefaultInt = DefaultInt(1), **kwargs: Any) -> "VideoStream":
        """

        11.95 fieldorder
        Transform the field order of the input video.

        It accepts the following parameters:


        The default value is ‘tff’.

        The transformation is done by shifting the picture content up or down
        by one line, and filling the remaining line with appropriate picture content.
        This method is consistent with most broadcast field order converters.

        If the input video is not flagged as being interlaced, or it is already
        flagged as being of the required output field order, then this filter does
        not alter the incoming video.

        It is very useful when converting to or from PAL DV material,
        which is bottom field first.

        For example:

        ffmpeg -i in.vob -vf "fieldorder=bff" out.dv

        Parameters:
        ----------

        :param int order: The output field order. Valid values are tff for top field first or bff for bottom field first.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#fieldorder

        """
        filter_node = FilterNode(
            name="fieldorder",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "order": order,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def fifo(self, **kwargs: Any) -> "VideoStream":
        """

        11.96 fifo, afifo
        Buffer input images and send them when they are requested.

        It is mainly useful when auto-inserted by the libavfilter
        framework.

        It does not take parameters.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#fifo_002c-afifo

        """
        filter_node = FilterNode(
            name="fifo",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def fillborders(
        self,
        *,
        left: int | DefaultInt = DefaultInt(0),
        right: int | DefaultInt = DefaultInt(0),
        top: int | DefaultInt = DefaultInt(0),
        bottom: int | DefaultInt = DefaultInt(0),
        mode: int
        | Literal["smear", "mirror", "fixed", "reflect", "wrap", "fade", "margins"]
        | DefaultStr = DefaultStr("smear"),
        color: str | DefaultStr = DefaultStr("black"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.97 fillborders
        Fill borders of the input video, without changing video stream dimensions.
        Sometimes video can have garbage at the four edges and you may not want to
        crop video input to keep size multiple of some number.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int left: Number of pixels to fill from left border.
        :param int right: Number of pixels to fill from right border.
        :param int top: Number of pixels to fill from top border.
        :param int bottom: Number of pixels to fill from bottom border.
        :param int mode: Set fill mode. It accepts the following values: ‘smear’ fill pixels using outermost pixels ‘mirror’ fill pixels using mirroring (half sample symmetric) ‘fixed’ fill pixels with constant value ‘reflect’ fill pixels using reflecting (whole sample symmetric) ‘wrap’ fill pixels using wrapping ‘fade’ fade pixels to constant value ‘margins’ fill pixels at top and bottom with weighted averages pixels near borders Default is smear.
        :param str color: Set color for pixels in fixed or fade mode. Default is black.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#fillborders

        """
        filter_node = FilterNode(
            name="fillborders",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "left": left,
                "right": right,
                "top": top,
                "bottom": bottom,
                "mode": mode,
                "color": color,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def find_rect(
        self,
        *,
        object: str,
        threshold: float | DefaultFloat = DefaultFloat(0.5),
        mipmaps: int | DefaultInt = DefaultInt(3),
        xmin: int | DefaultInt = DefaultInt(0),
        ymin: int | DefaultInt = DefaultInt(0),
        xmax: int | DefaultInt = DefaultInt(0),
        ymax: int | DefaultInt = DefaultInt(0),
        discard: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.98 find_rect
        Find a rectangular object in the input video.

        The object to search for must be specified as a gray8 image specified with the
        object option.

        For each possible match, a score is computed. If the score reaches the specified
        threshold, the object is considered found.

        If the input video contains multiple instances of the object, the filter will
        find only one of them.

        When an object is found, the following metadata entries are set in the matching
        frame:

        It accepts the following options:

        Parameters:
        ----------

        :param str object: Filepath of the object image, needs to be in gray8.
        :param float threshold: Detection threshold, expressed as a decimal number in the range 0-1. A threshold value of 0.01 means only exact matches, a threshold of 0.99 means almost everything matches. Default value is 0.5.
        :param int mipmaps: Number of mipmaps, default is 3.
        :param int xmin: Specifies the rectangle in which to search.
        :param int ymin: Specifies the rectangle in which to search.
        :param int xmax: Specifies the rectangle in which to search.
        :param int ymax: Specifies the rectangle in which to search.
        :param bool discard: Discard frames where object is not detected. Default is disabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#find_005frect

        """
        filter_node = FilterNode(
            name="find_rect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "object": object,
                "threshold": threshold,
                "mipmaps": mipmaps,
                "xmin": xmin,
                "ymin": ymin,
                "xmax": xmax,
                "ymax": ymax,
                "discard": discard,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def flip_vulkan(self, **kwargs: Any) -> "VideoStream":
        """

        14.8 flip_vulkan
        Flips an image along both the vertical and horizontal axis.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#flip_005fvulkan

        """
        filter_node = FilterNode(
            name="flip_vulkan",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def floodfill(
        self,
        *,
        x: int | DefaultInt = DefaultInt(0),
        y: int | DefaultInt = DefaultInt(0),
        s0: int | DefaultInt = DefaultInt(0),
        s1: int | DefaultInt = DefaultInt(0),
        s2: int | DefaultInt = DefaultInt(0),
        s3: int | DefaultInt = DefaultInt(0),
        d0: int | DefaultInt = DefaultInt(0),
        d1: int | DefaultInt = DefaultInt(0),
        d2: int | DefaultInt = DefaultInt(0),
        d3: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.99 floodfill
        Flood area with values of same pixel components with another values.

        It accepts the following options:

        Parameters:
        ----------

        :param int x: Set pixel x coordinate.
        :param int y: Set pixel y coordinate.
        :param int s0: Set source #0 component value.
        :param int s1: Set source #1 component value.
        :param int s2: Set source #2 component value.
        :param int s3: Set source #3 component value.
        :param int d0: Set destination #0 component value.
        :param int d1: Set destination #1 component value.
        :param int d2: Set destination #2 component value.
        :param int d3: Set destination #3 component value.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#floodfill

        """
        filter_node = FilterNode(
            name="floodfill",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "x": x,
                "y": y,
                "s0": s0,
                "s1": s1,
                "s2": s2,
                "s3": s3,
                "d0": d0,
                "d1": d1,
                "d2": d2,
                "d3": d3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def format(self, *, pix_fmts: str, **kwargs: Any) -> "VideoStream":
        """

        11.100 format
        Convert the input video to one of the specified pixel formats.
        Libavfilter will try to pick one that is suitable as input to
        the next filter.

        It accepts the following parameters:

        Parameters:
        ----------

        :param str pix_fmts: A ’|’-separated list of pixel format names, such as "pix_fmts=yuv420p|monow|rgb24".

        Ref: https://ffmpeg.org/ffmpeg-filters.html#format

        """
        filter_node = FilterNode(
            name="format",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "pix_fmts": pix_fmts,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def fps(
        self,
        *,
        fps: str | DefaultStr = DefaultStr("25"),
        start_time: float | DefaultFloat = DefaultFloat(1.7976931348623157e308),
        round: int | Literal["zero", "inf", "down", "up", "near"] | DefaultStr = DefaultStr("near"),
        eof_action: int | Literal["round", "pass"] | DefaultStr = DefaultStr("round"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.101 fps
        Convert the video to specified constant frame rate by duplicating or dropping
        frames as necessary.

        It accepts the following parameters:

        Alternatively, the options can be specified as a flat string:
        fps[:start_time[:round]].

        See also the setpts filter.

        Parameters:
        ----------

        :param str fps: The desired output frame rate. It accepts expressions containing the following constants: ‘source_fps’ The input’s frame rate ‘ntsc’ NTSC frame rate of 30000/1001 ‘pal’ PAL frame rate of 25.0 ‘film’ Film frame rate of 24.0 ‘ntsc_film’ NTSC-film frame rate of 24000/1001 The default is 25.
        :param float start_time: Assume the first PTS should be the given value, in seconds. This allows for padding/trimming at the start of stream. By default, no assumption is made about the first frame’s expected PTS, so no padding or trimming is done. For example, this could be set to 0 to pad the beginning with duplicates of the first frame if a video stream starts after the audio stream or to trim any frames with a negative PTS.
        :param int round: Timestamp (PTS) rounding method. Possible values are: zero round towards 0 inf round away from 0 down round towards -infinity up round towards +infinity near round to nearest The default is near.
        :param int eof_action: Action performed when reading the last frame. Possible values are: round Use same timestamp rounding method as used for other frames. pass Pass through last frame if input duration has not been reached yet. The default is round.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#fps

        """
        filter_node = FilterNode(
            name="fps",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "fps": fps,
                "start_time": start_time,
                "round": round,
                "eof_action": eof_action,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def framepack(
        self,
        _right: "VideoStream",
        *,
        format: int | Literal["sbs", "tab", "frameseq", "lines", "columns"] | DefaultStr = DefaultStr("sbs"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.102 framepack
        Pack two different video streams into a stereoscopic video, setting proper
        metadata on supported codecs. The two views should have the same size and
        framerate and processing will stop when the shorter video ends. Please note
        that you may conveniently adjust view properties with the scale and
        fps filters.

        It accepts the following parameters:

        Some examples:


        # Convert left and right views into a frame-sequential video
        ffmpeg -i LEFT -i RIGHT -filter_complex framepack=frameseq OUTPUT

        # Convert views into a side-by-side video with the same output resolution as the input
        ffmpeg -i LEFT -i RIGHT -filter_complex [0:v]scale=w=iw/2[left],[1:v]scale=w=iw/2[right],[left][right]framepack=sbs OUTPUT

        Parameters:
        ----------

        :param int format: The desired packing format. Supported values are: sbs The views are next to each other (default). tab The views are on top of each other. lines The views are packed by line. columns The views are packed by column. frameseq The views are temporally interleaved.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#framepack

        """
        filter_node = FilterNode(
            name="framepack",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _right,
            ],
            kwargs={
                "format": format,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def framerate(
        self,
        *,
        fps: str | DefaultStr = DefaultStr("50"),
        interp_start: int | DefaultInt = DefaultInt(15),
        interp_end: int | DefaultInt = DefaultInt(240),
        scene: float | DefaultFloat = DefaultFloat(8.2),
        flags: str | Literal["scene_change_detect", "scd"] | DefaultStr = DefaultStr("scene_change_detect"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.103 framerate
        Change the frame rate by interpolating new video output frames from the source
        frames.

        This filter is not designed to function correctly with interlaced media. If
        you wish to change the frame rate of interlaced media then you are required
        to deinterlace before this filter and re-interlace after this filter.

        A description of the accepted options follows.

        Parameters:
        ----------

        :param str fps: Specify the output frames per second. This option can also be specified as a value alone. The default is 50.
        :param int interp_start: Specify the start of a range where the output frame will be created as a linear interpolation of two frames. The range is [0-255], the default is 15.
        :param int interp_end: Specify the end of a range where the output frame will be created as a linear interpolation of two frames. The range is [0-255], the default is 240.
        :param float scene: Specify the level at which a scene change is detected as a value between 0 and 100 to indicate a new scene; a low value reflects a low probability for the current frame to introduce a new scene, while a higher value means the current frame is more likely to be one. The default is 8.2.
        :param str flags: Specify flags influencing the filter process. Available value for flags is: scene_change_detect, scd Enable scene change detection using the value of the option scene. This flag is enabled by default.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#framerate

        """
        filter_node = FilterNode(
            name="framerate",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "fps": fps,
                "interp_start": interp_start,
                "interp_end": interp_end,
                "scene": scene,
                "flags": flags,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def framestep(self, *, step: int | DefaultInt = DefaultInt(1), **kwargs: Any) -> "VideoStream":
        """

        11.104 framestep
        Select one frame every N-th frame.

        This filter accepts the following option:

        Parameters:
        ----------

        :param int step: Select frame after every step frames. Allowed values are positive integers higher than 0. Default value is 1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#framestep

        """
        filter_node = FilterNode(
            name="framestep",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "step": step,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def freezedetect(
        self, *, n: float | DefaultFloat = DefaultFloat(0.001), d: int | DefaultInt = DefaultInt(2000000), **kwargs: Any
    ) -> "VideoStream":
        """

        11.105 freezedetect
        Detect frozen video.

        This filter logs a message and sets frame metadata when it detects that the
        input video has no significant change in content during a specified duration.
        Video freeze detection calculates the mean average absolute difference of all
        the components of video frames and compares it to a noise floor.

        The printed times and duration are expressed in seconds. The
        lavfi.freezedetect.freeze_start metadata key is set on the first frame
        whose timestamp equals or exceeds the detection duration and it contains the
        timestamp of the first frame of the freeze. The
        lavfi.freezedetect.freeze_duration and
        lavfi.freezedetect.freeze_end metadata keys are set on the first frame
        after the freeze.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float n: Set noise tolerance. Can be specified in dB (in case "dB" is appended to the specified value) or as a difference ratio between 0 and 1. Default is -60dB, or 0.001.
        :param int d: Set freeze duration until notification (default is 2 seconds).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#freezedetect

        """
        filter_node = FilterNode(
            name="freezedetect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "n": n,
                "d": d,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def freezeframes(
        self,
        _replace: "VideoStream",
        *,
        first: int | DefaultInt = DefaultInt(0),
        last: int | DefaultInt = DefaultInt(0),
        replace: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.106 freezeframes
        Freeze video frames.

        This filter freezes video frames using frame from 2nd input.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int first: Set number of first frame from which to start freeze.
        :param int last: Set number of last frame from which to end freeze.
        :param int replace: Set number of frame from 2nd input which will be used instead of replaced frames.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#freezeframes

        """
        filter_node = FilterNode(
            name="freezeframes",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _replace,
            ],
            kwargs={
                "first": first,
                "last": last,
                "replace": replace,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def frei0r(self, *, filter_name: str, filter_params: str, **kwargs: Any) -> "VideoStream":
        """

        11.107 frei0r
        Apply a frei0r effect to the input video.

        To enable the compilation of this filter, you need to install the frei0r
        header and configure FFmpeg with --enable-frei0r.

        It accepts the following parameters:


        A frei0r effect parameter can be a boolean (its value is either
        "y" or "n"), a double, a color (specified as
        R/G/B, where R, G, and B are floating point
        numbers between 0.0 and 1.0, inclusive) or a color description as specified in the
        (ffmpeg-utils)"Color" section in the ffmpeg-utils manual,
        a position (specified as X/Y, where
        X and Y are floating point numbers) and/or a string.

        The number and types of parameters depend on the loaded effect. If an
        effect parameter is not specified, the default value is set.

        Parameters:
        ----------

        :param str filter_name: The name of the frei0r effect to load. If the environment variable FREI0R_PATH is defined, the frei0r effect is searched for in each of the directories specified by the colon-separated list in FREI0R_PATH. Otherwise, the standard frei0r paths are searched, in this order: HOME/.frei0r-1/lib/, /usr/local/lib/frei0r-1/, /usr/lib/frei0r-1/.
        :param str filter_params: A ’|’-separated list of parameters to pass to the frei0r effect.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#frei0r

        """
        filter_node = FilterNode(
            name="frei0r",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "filter_name": filter_name,
                "filter_params": filter_params,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def fspp(
        self,
        *,
        quality: int | DefaultInt = DefaultInt(4),
        qp: int | DefaultInt = DefaultInt(0),
        strength: int | DefaultInt = DefaultInt(0),
        use_bframe_qp: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.108 fspp
        Apply fast and simple postprocessing. It is a faster version of spp.

        It splits (I)DCT into horizontal/vertical passes. Unlike the simple post-
        processing filter, one of them is performed once per block, not per pixel.
        This allows for much higher speed.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int quality: Set quality. This option defines the number of levels for averaging. It accepts an integer in the range 4-5. Default value is 4.
        :param int qp: Force a constant quantization parameter. It accepts an integer in range 0-63. If not set, the filter will use the QP from the video stream (if available).
        :param int strength: Set filter strength. It accepts an integer in range -15 to 32. Lower values mean more details but also more artifacts, while higher values make the image smoother but also blurrier. Default value is 0 − PSNR optimal.
        :param bool use_bframe_qp: Enable the use of the QP from the B-Frames if set to 1. Using this option may cause flicker since the B-Frames have often larger QP. Default is 0 (not enabled).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#fspp

        """
        filter_node = FilterNode(
            name="fspp",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "quality": quality,
                "qp": qp,
                "strength": strength,
                "use_bframe_qp": use_bframe_qp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def gblur(
        self,
        *,
        sigma: float | DefaultFloat = DefaultFloat(0.5),
        steps: int | DefaultInt = DefaultInt(1),
        planes: int | DefaultStr = DefaultStr("0xF"),
        sigmaV: float | DefaultFloat = DefaultFloat(-1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.109 gblur
        Apply Gaussian blur filter.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float sigma: Set horizontal sigma, standard deviation of Gaussian blur. Default is 0.5.
        :param int steps: Set number of steps for Gaussian approximation. Default is 1.
        :param int planes: Set which planes to filter. By default all planes are filtered.
        :param float sigmaV: Set vertical sigma, if negative it will be same as sigma. Default is -1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#gblur

        """
        filter_node = FilterNode(
            name="gblur",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "sigma": sigma,
                "steps": steps,
                "planes": planes,
                "sigmaV": sigmaV,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def gblur_vulkan(
        self,
        *,
        sigma: float | DefaultFloat = DefaultFloat(0.5),
        sigmaV: float | DefaultFloat = DefaultFloat(0.0),
        planes: int | DefaultStr = DefaultStr("0xF"),
        size: int | DefaultInt = DefaultInt(19),
        sizeV: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        14.9 gblur_vulkan
        Apply Gaussian blur filter on Vulkan frames.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float sigma: Set horizontal sigma, standard deviation of Gaussian blur. Default is 0.5.
        :param float sigmaV: Set vertical sigma, if negative it will be same as sigma. Default is -1.
        :param int planes: Set which planes to filter. By default all planes are filtered.
        :param int size: Set the kernel size along the horizontal axis. Default is 19.
        :param int sizeV: Set the kernel size along the vertical axis. Default is 0, which sets to use the same value as size.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#gblur_005fvulkan

        """
        filter_node = FilterNode(
            name="gblur_vulkan",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "sigma": sigma,
                "sigmaV": sigmaV,
                "planes": planes,
                "size": size,
                "sizeV": sizeV,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def geq(
        self,
        *,
        lum_expr: str,
        cb_expr: str,
        cr_expr: str,
        alpha_expr: str,
        red_expr: str,
        green_expr: str,
        blue_expr: str,
        interpolation: int | Literal["nearest", "n", "bilinear", "b"] | DefaultStr = DefaultStr("bilinear"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.110 geq
        Apply generic equation to each pixel.

        The filter accepts the following options:


        The colorspace is selected according to the specified options. If one
        of the lum_expr, cb_expr, or cr_expr
        options is specified, the filter will automatically select a YCbCr
        colorspace. If one of the red_expr, green_expr, or
        blue_expr options is specified, it will select an RGB
        colorspace.

        If one of the chrominance expression is not defined, it falls back on the other
        one. If no alpha expression is specified it will evaluate to opaque value.
        If none of chrominance expressions are specified, they will evaluate
        to the luma expression.

        The expressions can use the following variables and functions:


        For functions, if x and y are outside the area, the value will be
        automatically clipped to the closer edge.

        Please note that this filter can use multiple threads in which case each slice
        will have its own expression state. If you want to use only a single expression
        state because your expressions depend on previous state then you should limit
        the number of filter threads to 1.

        Parameters:
        ----------

        :param str lum_expr: Set the luma expression.
        :param str cb_expr: Set the chrominance blue expression.
        :param str cr_expr: Set the chrominance red expression.
        :param str alpha_expr: Set the alpha expression.
        :param str red_expr: Set the red expression.
        :param str green_expr: Set the green expression.
        :param str blue_expr: Set the blue expression.
        :param int interpolation: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#geq

        """
        filter_node = FilterNode(
            name="geq",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "lum_expr": lum_expr,
                "cb_expr": cb_expr,
                "cr_expr": cr_expr,
                "alpha_expr": alpha_expr,
                "red_expr": red_expr,
                "green_expr": green_expr,
                "blue_expr": blue_expr,
                "interpolation": interpolation,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def gradfun(
        self,
        *,
        strength: float | DefaultFloat = DefaultFloat(1.2),
        radius: int | DefaultInt = DefaultInt(16),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.111 gradfun
        Fix the banding artifacts that are sometimes introduced into nearly flat
        regions by truncation to 8-bit color depth.
        Interpolate the gradients that should go where the bands are, and
        dither them.

        It is designed for playback only.  Do not use it prior to
        lossy compression, because compression tends to lose the dither and
        bring back the bands.

        It accepts the following parameters:


        Alternatively, the options can be specified as a flat string:
        strength[:radius]

        Parameters:
        ----------

        :param float strength: The maximum amount by which the filter will change any one pixel. This is also the threshold for detecting nearly flat regions. Acceptable values range from .51 to 64; the default value is 1.2. Out-of-range values will be clipped to the valid range.
        :param int radius: The neighborhood to fit the gradient to. A larger radius makes for smoother gradients, but also prevents the filter from modifying the pixels near detailed regions. Acceptable values are 8-32; the default value is 16. Out-of-range values will be clipped to the valid range.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#gradfun

        """
        filter_node = FilterNode(
            name="gradfun",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "strength": strength,
                "radius": radius,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def graphmonitor(
        self,
        *,
        size: str | DefaultStr = DefaultStr("hd720"),
        opacity: float | DefaultFloat = DefaultFloat(0.9),
        mode: str | Literal["full", "compact", "nozero", "noeof", "nodisabled"] | DefaultStr = DefaultStr(0),
        flags: str
        | Literal[
            "none",
            "all",
            "queue",
            "frame_count_in",
            "frame_count_out",
            "frame_count_delta",
            "pts",
            "pts_delta",
            "time",
            "time_delta",
            "timebase",
            "format",
            "size",
            "rate",
            "eof",
            "sample_count_in",
            "sample_count_out",
            "sample_count_delta",
            "disabled",
        ]
        | DefaultStr = DefaultStr("queue"),
        rate: str | DefaultStr = DefaultStr("25"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.112 graphmonitor
        Show various filtergraph stats.

        With this filter one can debug complete filtergraph.
        Especially issues with links filling with queued frames.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str size: Set video output size. Default is hd720.
        :param float opacity: Set video opacity. Default is 0.9. Allowed range is from 0 to 1.
        :param str mode: Set output mode flags. Available values for flags are: ‘full’ No any filtering. Default. ‘compact’ Show only filters with queued frames. ‘nozero’ Show only filters with non-zero stats. ‘noeof’ Show only filters with non-eof stat. ‘nodisabled’ Show only filters that are enabled in timeline.
        :param str flags: Set flags which enable which stats are shown in video. Available values for flags are: ‘none’ All flags turned off. ‘all’ All flags turned on. ‘queue’ Display number of queued frames in each link. ‘frame_count_in’ Display number of frames taken from filter. ‘frame_count_out’ Display number of frames given out from filter. ‘frame_count_delta’ Display delta number of frames between above two values. ‘pts’ Display current filtered frame pts. ‘pts_delta’ Display pts delta between current and previous frame. ‘time’ Display current filtered frame time. ‘time_delta’ Display time delta between current and previous frame. ‘timebase’ Display time base for filter link. ‘format’ Display used format for filter link. ‘size’ Display video size or number of audio channels in case of audio used by filter link. ‘rate’ Display video frame rate or sample rate in case of audio used by filter link. ‘eof’ Display link output status. ‘sample_count_in’ Display number of samples taken from filter. ‘sample_count_out’ Display number of samples given out from filter. ‘sample_count_delta’ Display delta number of samples between above two values. ‘disabled’ Show the timeline filter status.
        :param str rate: Set upper limit for video rate of output stream, Default value is 25. This guarantee that output video frame rate will not be higher than this value.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#graphmonitor

        """
        filter_node = FilterNode(
            name="graphmonitor",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "size": size,
                "opacity": opacity,
                "mode": mode,
                "flags": flags,
                "rate": rate,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def grayworld(self, **kwargs: Any) -> "VideoStream":
        """

        11.113 grayworld
        A color constancy filter that applies color correction based on the grayworld assumption

        See: https://www.researchgate.net/publication/275213614_A_New_Color_Correction_Method_for_Underwater_Imaging

        The algorithm  uses linear light, so input
        data should be linearized beforehand (and possibly correctly tagged).


        ffmpeg -i INPUT -vf zscale=transfer=linear,grayworld,zscale=transfer=bt709,format=yuv420p OUTPUT

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#grayworld

        """
        filter_node = FilterNode(
            name="grayworld",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def greyedge(
        self,
        *,
        difford: int | DefaultInt = DefaultInt(1),
        minknorm: int | DefaultInt = DefaultInt(1),
        sigma: float | DefaultFloat = DefaultFloat(1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.114 greyedge
        A color constancy variation filter which estimates scene illumination via grey edge algorithm
        and corrects the scene colors accordingly.

        See: https://staff.science.uva.nl/th.gevers/pub/GeversTIP07.pdf

        The filter accepts the following options:

        Parameters:
        ----------

        :param int difford: The order of differentiation to be applied on the scene. Must be chosen in the range [0,2] and default value is 1.
        :param int minknorm: The Minkowski parameter to be used for calculating the Minkowski distance. Must be chosen in the range [0,20] and default value is 1. Set to 0 for getting max value instead of calculating Minkowski distance.
        :param float sigma: The standard deviation of Gaussian blur to be applied on the scene. Must be chosen in the range [0,1024.0] and default value = 1. floor( sigma * break_off_sigma(3) ) can’t be equal to 0 if difford is greater than 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#greyedge

        """
        filter_node = FilterNode(
            name="greyedge",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "difford": difford,
                "minknorm": minknorm,
                "sigma": sigma,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def haldclut(
        self,
        _clut: "VideoStream",
        *,
        clut: int | Literal["first", "all"] | DefaultStr = DefaultStr("all"),
        interp: int
        | Literal["nearest", "trilinear", "tetrahedral", "pyramid", "prism"]
        | DefaultStr = DefaultStr("tetrahedral"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.116 haldclut
        Apply a Hald CLUT to a video stream.

        First input is the video stream to process, and second one is the Hald CLUT.
        The Hald CLUT input can be a simple picture or a complete video stream.

        The filter accepts the following options:


        haldclut also has the same interpolation options as lut3d (both
        filters share the same internals).

        This filter also supports the framesync options.

        More information about the Hald CLUT can be found on Eskil Steenberg’s website
        (Hald CLUT author) at http://www.quelsolaar.com/technology/clut.html.

        Parameters:
        ----------

        :param int clut: Set which CLUT video frames will be processed from second input stream, can be first or all. Default is all.
        :param int interp: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#haldclut

        """
        filter_node = FilterNode(
            name="haldclut",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _clut,
            ],
            kwargs={
                "clut": clut,
                "interp": interp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def hflip(self, **kwargs: Any) -> "VideoStream":
        """

        11.117 hflip
        Flip the input video horizontally.

        For example, to horizontally flip the input video with ffmpeg:

        ffmpeg -i in.avi -vf "hflip" out.avi

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#hflip

        """
        filter_node = FilterNode(
            name="hflip",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def hflip_vulkan(self, **kwargs: Any) -> "VideoStream":
        """

        14.7 hflip_vulkan
        Flips an image horizontally.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#hflip_005fvulkan

        """
        filter_node = FilterNode(
            name="hflip_vulkan",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def histeq(
        self,
        *,
        strength: float | DefaultFloat = DefaultFloat(0.2),
        intensity: float | DefaultFloat = DefaultFloat(0.21),
        antibanding: int | Literal["none", "weak", "strong"] | DefaultStr = DefaultStr("none"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.118 histeq
        This filter applies a global color histogram equalization on a
        per-frame basis.

        It can be used to correct video that has a compressed range of pixel
        intensities.  The filter redistributes the pixel intensities to
        equalize their distribution across the intensity range. It may be
        viewed as an "automatically adjusting contrast filter". This filter is
        useful only for correcting degraded or poorly captured source
        video.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float strength: Determine the amount of equalization to be applied. As the strength is reduced, the distribution of pixel intensities more-and-more approaches that of the input frame. The value must be a float number in the range [0,1] and defaults to 0.200.
        :param float intensity: Set the maximum intensity that can generated and scale the output values appropriately. The strength should be set as desired and then the intensity can be limited if needed to avoid washing-out. The value must be a float number in the range [0,1] and defaults to 0.210.
        :param int antibanding: Set the antibanding level. If enabled the filter will randomly vary the luminance of output pixels by a small amount to avoid banding of the histogram. Possible values are none, weak or strong. It defaults to none.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#histeq

        """
        filter_node = FilterNode(
            name="histeq",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "strength": strength,
                "intensity": intensity,
                "antibanding": antibanding,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def histogram(
        self,
        *,
        level_height: int | DefaultInt = DefaultInt(200),
        scale_height: int | DefaultInt = DefaultInt(12),
        display_mode: int | Literal["overlay", "parade", "stack"] | DefaultStr = DefaultStr("stack"),
        levels_mode: int | Literal["linear", "logarithmic"] | DefaultStr = DefaultStr("linear"),
        components: int | DefaultInt = DefaultInt(7),
        fgopacity: float | DefaultFloat = DefaultFloat(0.7),
        bgopacity: float | DefaultFloat = DefaultFloat(0.5),
        colors_mode: int
        | Literal[
            "whiteonblack",
            "blackonwhite",
            "whiteongray",
            "blackongray",
            "coloronblack",
            "coloronwhite",
            "colorongray",
            "blackoncolor",
            "whiteoncolor",
            "grayoncolor",
        ]
        | DefaultStr = DefaultStr("whiteonblack"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.119 histogram
        Compute and draw a color distribution histogram for the input video.

        The computed histogram is a representation of the color component
        distribution in an image.

        Standard histogram displays the color components distribution in an image.
        Displays color graph for each color component. Shows distribution of
        the Y, U, V, A or R, G, B components, depending on input format, in the
        current frame. Below each graph a color component scale meter is shown.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int level_height: Set height of level. Default value is 200. Allowed range is [50, 2048].
        :param int scale_height: Set height of color scale. Default value is 12. Allowed range is [0, 40].
        :param int display_mode: Set display mode. It accepts the following values: ‘stack’ Per color component graphs are placed below each other. ‘parade’ Per color component graphs are placed side by side. ‘overlay’ Presents information identical to that in the parade, except that the graphs representing color components are superimposed directly over one another. Default is stack.
        :param int levels_mode: Set mode. Can be either linear, or logarithmic. Default is linear.
        :param int components: Set what color components to display. Default is 7.
        :param float fgopacity: Set foreground opacity. Default is 0.7.
        :param float bgopacity: Set background opacity. Default is 0.5.
        :param int colors_mode: Set colors mode. It accepts the following values: ‘whiteonblack’ ‘blackonwhite’ ‘whiteongray’ ‘blackongray’ ‘coloronblack’ ‘coloronwhite’ ‘colorongray’ ‘blackoncolor’ ‘whiteoncolor’ ‘grayoncolor’ Default is whiteonblack.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#histogram

        """
        filter_node = FilterNode(
            name="histogram",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "level_height": level_height,
                "scale_height": scale_height,
                "display_mode": display_mode,
                "levels_mode": levels_mode,
                "components": components,
                "fgopacity": fgopacity,
                "bgopacity": bgopacity,
                "colors_mode": colors_mode,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def hqdn3d(
        self,
        *,
        luma_spatial: float | DefaultFloat = DefaultFloat(0.0),
        chroma_spatial: float | DefaultFloat = DefaultFloat(0.0),
        luma_tmp: float | DefaultFloat = DefaultFloat(0.0),
        chroma_tmp: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.120 hqdn3d
        This is a high precision/quality 3d denoise filter. It aims to reduce
        image noise, producing smooth images and making still images really
        still. It should enhance compressibility.

        It accepts the following optional parameters:

        Parameters:
        ----------

        :param float luma_spatial: A non-negative floating point number which specifies spatial luma strength. It defaults to 4.0.
        :param float chroma_spatial: A non-negative floating point number which specifies spatial chroma strength. It defaults to 3.0*luma_spatial/4.0.
        :param float luma_tmp: A floating point number which specifies luma temporal strength. It defaults to 6.0*luma_spatial/4.0.
        :param float chroma_tmp: A floating point number which specifies chroma temporal strength. It defaults to luma_tmp*chroma_spatial/luma_spatial.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#hqdn3d

        """
        filter_node = FilterNode(
            name="hqdn3d",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "luma_spatial": luma_spatial,
                "chroma_spatial": chroma_spatial,
                "luma_tmp": luma_tmp,
                "chroma_tmp": chroma_tmp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def hqx(self, *, n: int | DefaultInt = DefaultInt(3), **kwargs: Any) -> "VideoStream":
        """

        11.125 hqx
        Apply a high-quality magnification filter designed for pixel art. This filter
        was originally created by Maxim Stepin.

        It accepts the following option:

        Parameters:
        ----------

        :param int n: Set the scaling dimension: 2 for hq2x, 3 for hq3x and 4 for hq4x. Default is 3.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#hqx

        """
        filter_node = FilterNode(
            name="hqx",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "n": n,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def hsvhold(
        self,
        *,
        hue: float | DefaultFloat = DefaultFloat(0.0),
        sat: float | DefaultFloat = DefaultFloat(0.0),
        val: float | DefaultFloat = DefaultFloat(0.0),
        similarity: float | DefaultFloat = DefaultFloat(0.01),
        blend: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.127 hsvhold
        Turns a certain HSV range into gray values.

        This filter measures color difference between set HSV color in options
        and ones measured in video stream. Depending on options, output
        colors can be changed to be gray or not.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float hue: Set the hue value which will be used in color difference calculation. Allowed range is from -360 to 360. Default value is 0.
        :param float sat: Set the saturation value which will be used in color difference calculation. Allowed range is from -1 to 1. Default value is 0.
        :param float val: Set the value which will be used in color difference calculation. Allowed range is from -1 to 1. Default value is 0.
        :param float similarity: Set similarity percentage with the key color. Allowed range is from 0 to 1. Default value is 0.01. 0.00001 matches only the exact key color, while 1.0 matches everything.
        :param float blend: Blend percentage. Allowed range is from 0 to 1. Default value is 0. 0.0 makes pixels either fully gray, or not gray at all. Higher values result in more gray pixels, with a higher gray pixel the more similar the pixels color is to the key color.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#hsvhold

        """
        filter_node = FilterNode(
            name="hsvhold",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "hue": hue,
                "sat": sat,
                "val": val,
                "similarity": similarity,
                "blend": blend,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def hsvkey(
        self,
        *,
        hue: float | DefaultFloat = DefaultFloat(0.0),
        sat: float | DefaultFloat = DefaultFloat(0.0),
        val: float | DefaultFloat = DefaultFloat(0.0),
        similarity: float | DefaultFloat = DefaultFloat(0.01),
        blend: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.128 hsvkey
        Turns a certain HSV range into transparency.

        This filter measures color difference between set HSV color in options
        and ones measured in video stream. Depending on options, output
        colors can be changed to transparent by adding alpha channel.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float hue: Set the hue value which will be used in color difference calculation. Allowed range is from -360 to 360. Default value is 0.
        :param float sat: Set the saturation value which will be used in color difference calculation. Allowed range is from -1 to 1. Default value is 0.
        :param float val: Set the value which will be used in color difference calculation. Allowed range is from -1 to 1. Default value is 0.
        :param float similarity: Set similarity percentage with the key color. Allowed range is from 0 to 1. Default value is 0.01. 0.00001 matches only the exact key color, while 1.0 matches everything.
        :param float blend: Blend percentage. Allowed range is from 0 to 1. Default value is 0. 0.0 makes pixels either fully transparent, or not transparent at all. Higher values result in semi-transparent pixels, with a higher transparency the more similar the pixels color is to the key color.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#hsvkey

        """
        filter_node = FilterNode(
            name="hsvkey",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "hue": hue,
                "sat": sat,
                "val": val,
                "similarity": similarity,
                "blend": blend,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def hue(
        self,
        *,
        h: str,
        s: str | DefaultStr = DefaultStr("1"),
        H: str,
        b: str | DefaultStr = DefaultStr("0"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.129 hue
        Modify the hue and/or the saturation of the input.

        It accepts the following parameters:


        h and H are mutually exclusive, and can’t be
        specified at the same time.

        The b, h, H and s option values are
        expressions containing the following constants:

        Parameters:
        ----------

        :param str h: Specify the hue angle as a number of degrees. It accepts an expression, and defaults to "0".
        :param str s: Specify the saturation in the [-10,10] range. It accepts an expression and defaults to "1".
        :param str H: Specify the hue angle as a number of radians. It accepts an expression, and defaults to "0".
        :param str b: Specify the brightness in the [-10,10] range. It accepts an expression and defaults to "0".

        Ref: https://ffmpeg.org/ffmpeg-filters.html#hue

        """
        filter_node = FilterNode(
            name="hue",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "h": h,
                "s": s,
                "H": H,
                "b": b,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def huesaturation(
        self,
        *,
        hue: float | DefaultFloat = DefaultFloat(0.0),
        saturation: float | DefaultFloat = DefaultFloat(0.0),
        intensity: float | DefaultFloat = DefaultFloat(0.0),
        colors: str | Literal["r", "y", "g", "c", "b", "m", "a"] | DefaultStr = DefaultStr("a"),
        strength: float | DefaultFloat = DefaultFloat(1.0),
        rw: float | DefaultFloat = DefaultFloat(0.333),
        gw: float | DefaultFloat = DefaultFloat(0.334),
        bw: float | DefaultFloat = DefaultFloat(0.333),
        lightness: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.130 huesaturation
        Apply hue-saturation-intensity adjustments to input video stream.

        This filter operates in RGB colorspace.

        This filter accepts the following options:

        Parameters:
        ----------

        :param float hue: Set the hue shift in degrees to apply. Default is 0. Allowed range is from -180 to 180.
        :param float saturation: Set the saturation shift. Default is 0. Allowed range is from -1 to 1.
        :param float intensity: Set the intensity shift. Default is 0. Allowed range is from -1 to 1.
        :param str colors: Set which primary and complementary colors are going to be adjusted. This options is set by providing one or multiple values. This can select multiple colors at once. By default all colors are selected. ‘r’ Adjust reds. ‘y’ Adjust yellows. ‘g’ Adjust greens. ‘c’ Adjust cyans. ‘b’ Adjust blues. ‘m’ Adjust magentas. ‘a’ Adjust all colors.
        :param float strength: Set strength of filtering. Allowed range is from 0 to 100. Default value is 1.
        :param float rw: Set weight for each RGB component. Allowed range is from 0 to 1. By default is set to 0.333, 0.334, 0.333. Those options are used in saturation and lightess processing.
        :param float gw: Set weight for each RGB component. Allowed range is from 0 to 1. By default is set to 0.333, 0.334, 0.333. Those options are used in saturation and lightess processing.
        :param float bw: Set weight for each RGB component. Allowed range is from 0 to 1. By default is set to 0.333, 0.334, 0.333. Those options are used in saturation and lightess processing.
        :param bool lightness: Set preserving lightness, by default is disabled. Adjusting hues can change lightness from original RGB triplet, with this option enabled lightness is kept at same value.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#huesaturation

        """
        filter_node = FilterNode(
            name="huesaturation",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "hue": hue,
                "saturation": saturation,
                "intensity": intensity,
                "colors": colors,
                "strength": strength,
                "rw": rw,
                "gw": gw,
                "bw": bw,
                "lightness": lightness,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def hwdownload(self, **kwargs: Any) -> "VideoStream":
        """

        11.121 hwdownload
        Download hardware frames to system memory.

        The input must be in hardware frames, and the output a non-hardware format.
        Not all formats will be supported on the output - it may be necessary to insert
        an additional format filter immediately following in the graph to get
        the output in a supported format.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#hwdownload

        """
        filter_node = FilterNode(
            name="hwdownload",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def hwmap(
        self,
        *,
        mode: str
        | Literal["read", "write", "overwrite", "direct"]
        | DefaultStr = DefaultStr("AV_HWFRAME_MAP_READ | AV_HWFRAME_MAP_WRITE"),
        derive_device: str,
        reverse: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.122 hwmap
        Map hardware frames to system memory or to another device.

        This filter has several different modes of operation; which one is used depends
        on the input and output formats:

         Hardware frame input, normal frame output

        Map the input frames to system memory and pass them to the output.  If the
        original hardware frame is later required (for example, after overlaying
        something else on part of it), the hwmap filter can be used again
        in the next mode to retrieve it.
         Normal frame input, hardware frame output

        If the input is actually a software-mapped hardware frame, then unmap it -
        that is, return the original hardware frame.

        Otherwise, a device must be provided.  Create new hardware surfaces on that
        device for the output, then map them back to the software format at the input
        and give those frames to the preceding filter.  This will then act like the
        hwupload filter, but may be able to avoid an additional copy when
        the input is already in a compatible format.
         Hardware frame input and output

        A device must be supplied for the output, either directly or with the
        derive_device option.  The input and output devices must be of
        different types and compatible - the exact meaning of this is
        system-dependent, but typically it means that they must refer to the same
        underlying hardware context (for example, refer to the same graphics card).

        If the input frames were originally created on the output device, then unmap
        to retrieve the original frames.

        Otherwise, map the frames to the output device - create new hardware frames
        on the output corresponding to the frames on the input.

        The following additional parameters are accepted:

        Parameters:
        ----------

        :param str mode: Set the frame mapping mode. Some combination of: read The mapped frame should be readable. write The mapped frame should be writeable. overwrite The mapping will always overwrite the entire frame. This may improve performance in some cases, as the original contents of the frame need not be loaded. direct The mapping must not involve any copying. Indirect mappings to copies of frames are created in some cases where either direct mapping is not possible or it would have unexpected properties. Setting this flag ensures that the mapping is direct and will fail if that is not possible. Defaults to read+write if not specified.
        :param str derive_device: Rather than using the device supplied at initialisation, instead derive a new device of type type from the device the input frames exist on.
        :param int reverse: In a hardware to hardware mapping, map in reverse - create frames in the sink and map them back to the source. This may be necessary in some cases where a mapping in one direction is required but only the opposite direction is supported by the devices being used. This option is dangerous - it may break the preceding filter in undefined ways if there are any additional constraints on that filter’s output. Do not use it without fully understanding the implications of its use.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#hwmap

        """
        filter_node = FilterNode(
            name="hwmap",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "derive_device": derive_device,
                "reverse": reverse,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def hwupload(self, *, derive_device: str, **kwargs: Any) -> "VideoStream":
        """

        11.123 hwupload
        Upload system memory frames to hardware surfaces.

        The device to upload to must be supplied when the filter is initialised.  If
        using ffmpeg, select the appropriate device with the -filter_hw_device
        option or with the derive_device option.  The input and output devices
        must be of different types and compatible - the exact meaning of this is
        system-dependent, but typically it means that they must refer to the same
        underlying hardware context (for example, refer to the same graphics card).

        The following additional parameters are accepted:

        Parameters:
        ----------

        :param str derive_device: Rather than using the device supplied at initialisation, instead derive a new device of type type from the device the input frames exist on.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#hwupload

        """
        filter_node = FilterNode(
            name="hwupload",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "derive_device": derive_device,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def hwupload_cuda(self, *, device: int | DefaultInt = DefaultInt(0), **kwargs: Any) -> "VideoStream":
        """

        11.124 hwupload_cuda
        Upload system memory frames to a CUDA device.

        It accepts the following optional parameters:

        Parameters:
        ----------

        :param int device: The number of the CUDA device to use

        Ref: https://ffmpeg.org/ffmpeg-filters.html#hwupload_005fcuda

        """
        filter_node = FilterNode(
            name="hwupload_cuda",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "device": device,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def hysteresis(
        self,
        _alt: "VideoStream",
        *,
        planes: int | DefaultStr = DefaultStr("0xF"),
        threshold: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.131 hysteresis
        Grow first stream into second stream by connecting components.
        This makes it possible to build more robust edge masks.

        This filter accepts the following options:


        The hysteresis filter also supports the framesync options.

        Parameters:
        ----------

        :param int planes: Set which planes will be processed as bitmap, unprocessed planes will be copied from first stream. By default value 0xf, all planes will be processed.
        :param int threshold: Set threshold which is used in filtering. If pixel component value is higher than this value filter algorithm for connecting components is activated. By default value is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#hysteresis

        """
        filter_node = FilterNode(
            name="hysteresis",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _alt,
            ],
            kwargs={
                "planes": planes,
                "threshold": threshold,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def iccdetect(self, *, force: bool | DefaultInt = DefaultInt(1), **kwargs: Any) -> "VideoStream":
        """

        11.132 iccdetect
        Detect the colorspace  from an embedded ICC profile (if present), and update
        the frame’s tags accordingly.

        This filter accepts the following options:

        Parameters:
        ----------

        :param bool force: If true, the frame’s existing colorspace tags will always be overridden by values detected from an ICC profile. Otherwise, they will only be assigned if they contain unknown. Enabled by default.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#iccdetect

        """
        filter_node = FilterNode(
            name="iccdetect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "force": force,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def iccgen(
        self,
        *,
        color_primaries: int
        | Literal[
            "auto",
            "bt709",
            "bt470m",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "film",
            "bt2020",
            "smpte428",
            "smpte431",
            "smpte432",
            "jedec-p22",
            "ebu3213",
        ]
        | DefaultStr = DefaultStr("auto"),
        color_trc: int
        | Literal[
            "auto",
            "bt709",
            "bt470m",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "linear",
            "iec61966-2-4",
            "bt1361e",
            "iec61966-2-1",
            "bt2020-10",
            "bt2020-12",
            "smpte2084",
            "arib-std-b67",
        ]
        | DefaultStr = DefaultStr("auto"),
        force: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.133 iccgen
        Generate ICC profiles and attach them to frames.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int color_primaries: Configure the colorspace that the ICC profile will be generated for. The default value of auto infers the value from the input frame’s metadata, defaulting to BT.709/sRGB as appropriate. See the setparams filter for a list of possible values, but note that unknown are not valid values for this filter.
        :param int color_trc: Configure the colorspace that the ICC profile will be generated for. The default value of auto infers the value from the input frame’s metadata, defaulting to BT.709/sRGB as appropriate. See the setparams filter for a list of possible values, but note that unknown are not valid values for this filter.
        :param bool force: If true, an ICC profile will be generated even if it would overwrite an already existing ICC profile. Disabled by default.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#iccgen

        """
        filter_node = FilterNode(
            name="iccgen",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "color_primaries": color_primaries,
                "color_trc": color_trc,
                "force": force,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def identity(self, _reference: "VideoStream", **kwargs: Any) -> "VideoStream":
        """

        11.134 identity
        Obtain the identity score between two input videos.

        This filter takes two input videos.

        Both input videos must have the same resolution and pixel format for
        this filter to work correctly. Also it assumes that both inputs
        have the same number of frames, which are compared one by one.

        The obtained per component, average, min and max identity score is printed through
        the logging system.

        The filter stores the calculated identity scores of each frame in frame metadata.

        This filter also supports the framesync options.

        In the below example the input file main.mpg being processed is compared
        with the reference file ref.mpg.


        ffmpeg -i main.mpg -i ref.mpg -lavfi identity -f null -

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#identity

        """
        filter_node = FilterNode(
            name="identity",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _reference,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def idet(
        self,
        *,
        intl_thres: float | DefaultFloat = DefaultFloat(1.04),
        prog_thres: float | DefaultFloat = DefaultFloat(1.5),
        rep_thres: float | DefaultFloat = DefaultFloat(3.0),
        half_life: float | DefaultFloat = DefaultFloat(0.0),
        analyze_interlaced_flag: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.135 idet
        Detect video interlacing type.

        This filter tries to detect if the input frames are interlaced, progressive,
        top or bottom field first. It will also try to detect fields that are
        repeated between adjacent frames (a sign of telecine).

        Single frame detection considers only immediately adjacent frames when classifying each frame.
        Multiple frame detection incorporates the classification history of previous frames.

        The filter will log these metadata values:


        The filter accepts the following options:

        Parameters:
        ----------

        :param float intl_thres: Set interlacing threshold.
        :param float prog_thres: Set progressive threshold.
        :param float rep_thres: Threshold for repeated field detection.
        :param float half_life: Number of frames after which a given frame’s contribution to the statistics is halved (i.e., it contributes only 0.5 to its classification). The default of 0 means that all frames seen are given full weight of 1.0 forever.
        :param int analyze_interlaced_flag: When this is not 0 then idet will use the specified number of frames to determine if the interlaced flag is accurate, it will not count undetermined frames. If the flag is found to be accurate it will be used without any further computations, if it is found to be inaccurate it will be cleared without any further computations. This allows inserting the idet filter as a low computational method to clean up the interlaced flag

        Ref: https://ffmpeg.org/ffmpeg-filters.html#idet

        """
        filter_node = FilterNode(
            name="idet",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "intl_thres": intl_thres,
                "prog_thres": prog_thres,
                "rep_thres": rep_thres,
                "half_life": half_life,
                "analyze_interlaced_flag": analyze_interlaced_flag,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def il(
        self,
        *,
        luma_mode: int | Literal["none", "interleave", "i", "deinterleave", "d"] | DefaultStr = DefaultStr("none"),
        chroma_mode: int | Literal["none", "interleave", "i", "deinterleave", "d"] | DefaultStr = DefaultStr("none"),
        alpha_mode: int | Literal["none", "interleave", "i", "deinterleave", "d"] | DefaultStr = DefaultStr("none"),
        luma_swap: bool | DefaultInt = DefaultInt(0),
        chroma_swap: bool | DefaultInt = DefaultInt(0),
        alpha_swap: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.136 il
        Deinterleave or interleave fields.

        This filter allows one to process interlaced images fields without
        deinterlacing them. Deinterleaving splits the input frame into 2
        fields (so called half pictures). Odd lines are moved to the top
        half of the output image, even lines to the bottom half.
        You can process (filter) them independently and then re-interleave them.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int luma_mode: Available values for luma_mode, chroma_mode and alpha_mode are: ‘none’ Do nothing. ‘deinterleave, d’ Deinterleave fields, placing one above the other. ‘interleave, i’ Interleave fields. Reverse the effect of deinterleaving. Default value is none.
        :param int chroma_mode: Available values for luma_mode, chroma_mode and alpha_mode are: ‘none’ Do nothing. ‘deinterleave, d’ Deinterleave fields, placing one above the other. ‘interleave, i’ Interleave fields. Reverse the effect of deinterleaving. Default value is none.
        :param int alpha_mode: Available values for luma_mode, chroma_mode and alpha_mode are: ‘none’ Do nothing. ‘deinterleave, d’ Deinterleave fields, placing one above the other. ‘interleave, i’ Interleave fields. Reverse the effect of deinterleaving. Default value is none.
        :param bool luma_swap: Swap luma/chroma/alpha fields. Exchange even & odd lines. Default value is 0.
        :param bool chroma_swap: Swap luma/chroma/alpha fields. Exchange even & odd lines. Default value is 0.
        :param bool alpha_swap: Swap luma/chroma/alpha fields. Exchange even & odd lines. Default value is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#il

        """
        filter_node = FilterNode(
            name="il",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "luma_mode": luma_mode,
                "chroma_mode": chroma_mode,
                "alpha_mode": alpha_mode,
                "luma_swap": luma_swap,
                "chroma_swap": chroma_swap,
                "alpha_swap": alpha_swap,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def inflate(
        self,
        *,
        threshold0: int | DefaultInt = DefaultInt(65535),
        threshold1: int | DefaultInt = DefaultInt(65535),
        threshold2: int | DefaultInt = DefaultInt(65535),
        threshold3: int | DefaultInt = DefaultInt(65535),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.137 inflate
        Apply inflate effect to the video.

        This filter replaces the pixel by the local(3x3) average by taking into account
        only values higher than the pixel.

        It accepts the following options:

        Parameters:
        ----------

        :param int threshold0: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold1: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold2: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.
        :param int threshold3: Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#inflate

        """
        filter_node = FilterNode(
            name="inflate",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "threshold0": threshold0,
                "threshold1": threshold1,
                "threshold2": threshold2,
                "threshold3": threshold3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def interlace(
        self,
        *,
        scan: int | DefaultStr = DefaultStr("MODE_TFF"),
        lowpass: int | Literal["off", "linear", "complex"] | DefaultStr = DefaultStr("linear"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.138 interlace
        Simple interlacing filter from progressive contents. This interleaves upper (or
        lower) lines from odd frames with lower (or upper) lines from even frames,
        halving the frame rate and preserving image height.


           Original        Original             New Frame
           Frame 'j'      Frame 'j+1'             (tff)
          ==========      ===========       ==================
            Line 0  -------------------->    Frame 'j' Line 0
            Line 1          Line 1  ---->   Frame 'j+1' Line 1
            Line 2 --------------------->    Frame 'j' Line 2
            Line 3          Line 3  ---->   Frame 'j+1' Line 3
             ...             ...                   ...
        New Frame + 1 will be generated by Frame 'j+2' and Frame 'j+3' and so on

        It accepts the following optional parameters:

        Parameters:
        ----------

        :param int scan: This determines whether the interlaced frame is taken from the even (tff - default) or odd (bff) lines of the progressive frame.
        :param int lowpass: Vertical lowpass filter to avoid twitter interlacing and reduce moire patterns. ‘0, off’ Disable vertical lowpass filter ‘1, linear’ Enable linear filter (default) ‘2, complex’ Enable complex filter. This will slightly less reduce twitter and moire but better retain detail and subjective sharpness impression.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#interlace

        """
        filter_node = FilterNode(
            name="interlace",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "scan": scan,
                "lowpass": lowpass,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def kerndeint(
        self,
        *,
        thresh: int | DefaultInt = DefaultInt(10),
        map: bool | DefaultInt = DefaultInt(0),
        order: bool | DefaultInt = DefaultInt(0),
        sharp: bool | DefaultInt = DefaultInt(0),
        twoway: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.139 kerndeint
        Deinterlace input video by applying Donald Graft’s adaptive kernel
        deinterling. Work on interlaced parts of a video to produce
        progressive frames.

        The description of the accepted parameters follows.

        Parameters:
        ----------

        :param int thresh: Set the threshold which affects the filter’s tolerance when determining if a pixel line must be processed. It must be an integer in the range [0,255] and defaults to 10. A value of 0 will result in applying the process on every pixels.
        :param bool map: Paint pixels exceeding the threshold value to white if set to 1. Default is 0.
        :param bool order: Set the fields order. Swap fields if set to 1, leave fields alone if 0. Default is 0.
        :param bool sharp: Enable additional sharpening if set to 1. Default is 0.
        :param bool twoway: Enable twoway sharpening if set to 1. Default is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#kerndeint

        """
        filter_node = FilterNode(
            name="kerndeint",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "thresh": thresh,
                "map": map,
                "order": order,
                "sharp": sharp,
                "twoway": twoway,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def kirsch(
        self,
        *,
        planes: int | DefaultInt = DefaultInt(15),
        scale: float | DefaultFloat = DefaultFloat(1.0),
        delta: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.140 kirsch
        Apply kirsch operator to input video stream.

        The filter accepts the following option:

        Parameters:
        ----------

        :param int planes: Set which planes will be processed, unprocessed planes will be copied. By default value 0xf, all planes will be processed.
        :param float scale: Set value which will be multiplied with filtered result.
        :param float delta: Set value which will be added to filtered result.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#kirsch

        """
        filter_node = FilterNode(
            name="kirsch",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "planes": planes,
                "scale": scale,
                "delta": delta,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def lagfun(
        self,
        *,
        decay: float | DefaultFloat = DefaultFloat(0.95),
        planes: str | DefaultStr = DefaultStr(15),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.141 lagfun
        Slowly update darker pixels.

        This filter makes short flashes of light appear longer.
        This filter accepts the following options:

        Parameters:
        ----------

        :param float decay: Set factor for decaying. Default is .95. Allowed range is from 0 to 1.
        :param str planes: Set which planes to filter. Default is all. Allowed range is from 0 to 15.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lagfun

        """
        filter_node = FilterNode(
            name="lagfun",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "decay": decay,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def latency(self, **kwargs: Any) -> "VideoStream":
        """

        18.12 latency, alatency
        Measure filtering latency.

        Report previous filter filtering latency, delay in number of audio samples for audio filters
        or number of video frames for video filters.

        On end of input stream, filter will report min and max measured latency for previous running filter
        in filtergraph.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#latency_002c-alatency

        """
        filter_node = FilterNode(
            name="latency",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def lenscorrection(
        self,
        *,
        cx: float | DefaultFloat = DefaultFloat(0.5),
        cy: float | DefaultFloat = DefaultFloat(0.5),
        k1: float | DefaultFloat = DefaultFloat(0.0),
        k2: float | DefaultFloat = DefaultFloat(0.0),
        i: int | Literal["nearest", "bilinear"] | DefaultStr = DefaultStr("nearest"),
        fc: str | DefaultStr = DefaultStr("black@0"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.142 lenscorrection
        Correct radial lens distortion

        This filter can be used to correct for radial distortion as can result from the use
        of wide angle lenses, and thereby re-rectify the image. To find the right parameters
        one can use tools available for example as part of opencv or simply trial-and-error.
        To use opencv use the calibration sample (under samples/cpp) from the opencv sources
        and extract the k1 and k2 coefficients from the resulting matrix.

        Note that effectively the same filter is available in the open-source tools Krita and
        Digikam from the KDE project.

        In contrast to the vignette filter, which can also be used to compensate lens errors,
        this filter corrects the distortion of the image, whereas vignette corrects the
        brightness distribution, so you may want to use both filters together in certain
        cases, though you will have to take care of ordering, i.e. whether vignetting should
        be applied before or after lens correction.

        Parameters:
        ----------

        :param float cx: None
        :param float cy: None
        :param float k1: None
        :param float k2: None
        :param int i: None
        :param str fc: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lenscorrection

        """
        filter_node = FilterNode(
            name="lenscorrection",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "cx": cx,
                "cy": cy,
                "k1": k1,
                "k2": k2,
                "i": i,
                "fc": fc,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def lensfun(
        self,
        *,
        make: str,
        model: str,
        lens_model: str,
        db_path: str,
        mode: int
        | Literal["vignetting", "geometry", "subpixel", "vig_geo", "vig_subpixel", "distortion", "all"]
        | DefaultStr = DefaultStr("geometry"),
        focal_length: float | DefaultFloat = DefaultFloat(18.0),
        aperture: float | DefaultFloat = DefaultFloat(3.5),
        focus_distance: float | DefaultStr = DefaultStr("1000.0f"),
        scale: float | DefaultFloat = DefaultFloat(0.0),
        target_geometry: int
        | Literal[
            "rectilinear",
            "fisheye",
            "panoramic",
            "equirectangular",
            "fisheye_orthographic",
            "fisheye_stereographic",
            "fisheye_equisolid",
            "fisheye_thoby",
        ]
        | DefaultStr = DefaultStr("rectilinear"),
        reverse: bool | DefaultInt = DefaultInt(0),
        interpolation: int | Literal["nearest", "linear", "lanczos"] | DefaultStr = DefaultStr("linear"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.143 lensfun
        Apply lens correction via the lensfun library (http://lensfun.sourceforge.net/).

        The lensfun filter requires the camera make, camera model, and lens model
        to apply the lens correction. The filter will load the lensfun database and
        query it to find the corresponding camera and lens entries in the database. As
        long as these entries can be found with the given options, the filter can
        perform corrections on frames. Note that incomplete strings will result in the
        filter choosing the best match with the given options, and the filter will
        output the chosen camera and lens models (logged with level "info"). You must
        provide the make, camera model, and lens model as they are required.

        To obtain a list of available makes and models, leave out one or both of make and
        model options. The filter will send the full list to the log with level INFO.
        The first column is the make and the second column is the model.
        To obtain a list of available lenses, set any values for make and model and leave out the
        lens_model option. The filter will send the full list of lenses in the log with level
        INFO. The ffmpeg tool will exit after the list is printed.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str make: The make of the camera (for example, "Canon"). This option is required.
        :param str model: The model of the camera (for example, "Canon EOS 100D"). This option is required.
        :param str lens_model: The model of the lens (for example, "Canon EF-S 18-55mm f/3.5-5.6 IS STM"). This option is required.
        :param str db_path: The full path to the lens database folder. If not set, the filter will attempt to load the database from the install path when the library was built. Default is unset.
        :param int mode: The type of correction to apply. The following values are valid options: ‘vignetting’ Enables fixing lens vignetting. ‘geometry’ Enables fixing lens geometry. This is the default. ‘subpixel’ Enables fixing chromatic aberrations. ‘vig_geo’ Enables fixing lens vignetting and lens geometry. ‘vig_subpixel’ Enables fixing lens vignetting and chromatic aberrations. ‘distortion’ Enables fixing both lens geometry and chromatic aberrations. ‘all’ Enables all possible corrections.
        :param float focal_length: The focal length of the image/video (zoom; expected constant for video). For example, a 18–55mm lens has focal length range of [18–55], so a value in that range should be chosen when using that lens. Default 18.
        :param float aperture: The aperture of the image/video (expected constant for video). Note that aperture is only used for vignetting correction. Default 3.5.
        :param float focus_distance: The focus distance of the image/video (expected constant for video). Note that focus distance is only used for vignetting and only slightly affects the vignetting correction process. If unknown, leave it at the default value (which is 1000).
        :param float scale: The scale factor which is applied after transformation. After correction the video is no longer necessarily rectangular. This parameter controls how much of the resulting image is visible. The value 0 means that a value will be chosen automatically such that there is little or no unmapped area in the output image. 1.0 means that no additional scaling is done. Lower values may result in more of the corrected image being visible, while higher values may avoid unmapped areas in the output.
        :param int target_geometry: The target geometry of the output image/video. The following values are valid options: ‘rectilinear (default)’ ‘fisheye’ ‘panoramic’ ‘equirectangular’ ‘fisheye_orthographic’ ‘fisheye_stereographic’ ‘fisheye_equisolid’ ‘fisheye_thoby’
        :param bool reverse: Apply the reverse of image correction (instead of correcting distortion, apply it).
        :param int interpolation: The type of interpolation used when correcting distortion. The following values are valid options: ‘nearest’ ‘linear (default)’ ‘lanczos’

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lensfun

        """
        filter_node = FilterNode(
            name="lensfun",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "make": make,
                "model": model,
                "lens_model": lens_model,
                "db_path": db_path,
                "mode": mode,
                "focal_length": focal_length,
                "aperture": aperture,
                "focus_distance": focus_distance,
                "scale": scale,
                "target_geometry": target_geometry,
                "reverse": reverse,
                "interpolation": interpolation,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def libvmaf(
        self,
        _reference: "VideoStream",
        *,
        log_path: str,
        log_fmt: str | DefaultStr = DefaultStr("xml"),
        pool: str,
        n_threads: int | DefaultInt = DefaultInt(0),
        n_subsample: int | DefaultInt = DefaultInt(1),
        model: str | DefaultStr = DefaultStr("version=vmaf_v0.6.1"),
        feature: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.145 libvmaf
        Calculate the VMAF (Video Multi-Method Assessment Fusion) score for a
        reference/distorted pair of input videos.

        The first input is the distorted video, and the second input is the reference video.

        The obtained VMAF score is printed through the logging system.

        It requires Netflix’s vmaf library (libvmaf) as a pre-requisite.
        After installing the library it can be enabled using:
        ./configure --enable-libvmaf.

        The filter has following options:


        This filter also supports the framesync options.

        Parameters:
        ----------

        :param str log_path: Set the file path to be used to store log files.
        :param str log_fmt: Set the format of the log file (xml, json, csv, or sub).
        :param str pool: Set the pool method to be used for computing vmaf. Options are min, harmonic_mean or mean (default).
        :param int n_threads: Set number of threads to be used when initializing libvmaf. Default value: 0, no threads.
        :param int n_subsample: Set frame subsampling interval to be used.
        :param str model: A ‘|‘ delimited list of vmaf models. Each model can be configured with a number of parameters. Default value: "version=vmaf_v0.6.1"
        :param str feature: A ‘|‘ delimited list of features. Each feature can be configured with a number of parameters.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#libvmaf

        """
        filter_node = FilterNode(
            name="libvmaf",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _reference,
            ],
            kwargs={
                "log_path": log_path,
                "log_fmt": log_fmt,
                "pool": pool,
                "n_threads": n_threads,
                "n_subsample": n_subsample,
                "model": model,
                "feature": feature,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def libvmaf_cuda(
        self,
        _reference: "VideoStream",
        *,
        log_path: str,
        log_fmt: str | DefaultStr = DefaultStr("xml"),
        pool: str,
        n_threads: int | DefaultInt = DefaultInt(0),
        n_subsample: int | DefaultInt = DefaultInt(1),
        model: str | DefaultStr = DefaultStr("version=vmaf_v0.6.1"),
        feature: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.146 libvmaf_cuda
        This is the CUDA variant of the libvmaf filter. It only accepts CUDA frames.

        It requires Netflix’s vmaf library (libvmaf) as a pre-requisite.
        After installing the library it can be enabled using:
        ./configure --enable-nonfree --enable-ffnvcodec --enable-libvmaf.

        Parameters:
        ----------

        :param str log_path: None
        :param str log_fmt: None
        :param str pool: None
        :param int n_threads: None
        :param int n_subsample: None
        :param str model: None
        :param str feature: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#libvmaf_005fcuda

        """
        filter_node = FilterNode(
            name="libvmaf_cuda",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _reference,
            ],
            kwargs={
                "log_path": log_path,
                "log_fmt": log_fmt,
                "pool": pool,
                "n_threads": n_threads,
                "n_subsample": n_subsample,
                "model": model,
                "feature": feature,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def limiter(
        self,
        *,
        min: int | DefaultInt = DefaultInt(0),
        max: int | DefaultInt = DefaultInt(65535),
        planes: int | DefaultInt = DefaultInt(15),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.148 limiter
        Limits the pixel components values to the specified range [min, max].

        The filter accepts the following options:

        Parameters:
        ----------

        :param int min: Lower bound. Defaults to the lowest allowed value for the input.
        :param int max: Upper bound. Defaults to the highest allowed value for the input.
        :param int planes: Specify which planes will be processed. Defaults to all available.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#limiter

        """
        filter_node = FilterNode(
            name="limiter",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "min": min,
                "max": max,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def loop(
        self,
        *,
        loop: int | DefaultInt = DefaultInt(0),
        size: int | DefaultInt = DefaultInt(0),
        start: int | DefaultInt = DefaultInt(0),
        time: int | DefaultStr = DefaultStr("9223372036854775807LL"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.149 loop
        Loop video frames.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int loop: Set the number of loops. Setting this value to -1 will result in infinite loops. Default is 0.
        :param int size: Set maximal size in number of frames. Default is 0.
        :param int start: Set first frame of loop. Default is 0.
        :param int time: Set the time of loop start in seconds. Only used if option named start is set to -1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#loop

        """
        filter_node = FilterNode(
            name="loop",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "loop": loop,
                "size": size,
                "start": start,
                "time": time,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def lumakey(
        self,
        *,
        threshold: float | DefaultFloat = DefaultFloat(0.0),
        tolerance: float | DefaultFloat = DefaultFloat(0.01),
        softness: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.152 lumakey
        Turn certain luma values into transparency.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float threshold: Set the luma which will be used as base for transparency. Default value is 0.
        :param float tolerance: Set the range of luma values to be keyed out. Default value is 0.01.
        :param float softness: Set the range of softness. Default value is 0. Use this to control gradual transition from zero to full transparency.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lumakey

        """
        filter_node = FilterNode(
            name="lumakey",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "threshold": threshold,
                "tolerance": tolerance,
                "softness": softness,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def lut(
        self,
        *,
        c0: str | DefaultStr = DefaultStr("clipval"),
        c1: str | DefaultStr = DefaultStr("clipval"),
        c2: str | DefaultStr = DefaultStr("clipval"),
        c3: str | DefaultStr = DefaultStr("clipval"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.153 lut, lutrgb, lutyuv
        Compute a look-up table for binding each pixel component input value
        to an output value, and apply it to the input video.

        lutyuv applies a lookup table to a YUV input video, lutrgb
        to an RGB input video.

        These filters accept the following parameters:

        Each of them specifies the expression to use for computing the lookup table for
        the corresponding pixel component values.

        The exact component associated to each of the c* options depends on the
        format in input.

        The lut filter requires either YUV or RGB pixel formats in input,
        lutrgb requires RGB pixel formats in input, and lutyuv requires YUV.

        The expressions can contain the following constants and functions:


        All expressions default to "clipval".

        Parameters:
        ----------

        :param str c0: set first pixel component expression
        :param str c1: set second pixel component expression
        :param str c2: set third pixel component expression
        :param str c3: set fourth pixel component expression, corresponds to the alpha component

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lut_002c-lutrgb_002c-lutyuv

        """
        filter_node = FilterNode(
            name="lut",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "c0": c0,
                "c1": c1,
                "c2": c2,
                "c3": c3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def lut1d(
        self,
        *,
        file: str,
        interp: int | Literal["nearest", "linear", "cosine", "cubic", "spline"] | DefaultStr = DefaultStr("linear"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.150 lut1d
        Apply a 1D LUT to an input video.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str file: Set the 1D LUT file name. Currently supported formats: ‘cube’ Iridas ‘csp’ cineSpace
        :param int interp: Select interpolation mode. Available values are: ‘nearest’ Use values from the nearest defined point. ‘linear’ Interpolate values using the linear interpolation. ‘cosine’ Interpolate values using the cosine interpolation. ‘cubic’ Interpolate values using the cubic interpolation. ‘spline’ Interpolate values using the spline interpolation.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lut1d

        """
        filter_node = FilterNode(
            name="lut1d",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "file": file,
                "interp": interp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def lut2(
        self,
        _srcy: "VideoStream",
        *,
        c0: str | DefaultStr = DefaultStr("x"),
        c1: str | DefaultStr = DefaultStr("x"),
        c2: str | DefaultStr = DefaultStr("x"),
        c3: str | DefaultStr = DefaultStr("x"),
        d: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.154 lut2, tlut2
        The lut2 filter takes two input streams and outputs one
        stream.

        The tlut2 (time lut2) filter takes two consecutive frames
        from one single stream.

        This filter accepts the following parameters:

        The lut2 filter also supports the framesync options.

        Each of them specifies the expression to use for computing the lookup table for
        the corresponding pixel component values.

        The exact component associated to each of the c* options depends on the
        format in inputs.

        The expressions can contain the following constants:


        All expressions default to "x".

        Parameters:
        ----------

        :param str c0: set first pixel component expression
        :param str c1: set second pixel component expression
        :param str c2: set third pixel component expression
        :param str c3: set fourth pixel component expression, corresponds to the alpha component
        :param int d: set output bit depth, only available for lut2 filter. By default is 0, which means bit depth is automatically picked from first input format.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lut2_002c-tlut2

        """
        filter_node = FilterNode(
            name="lut2",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _srcy,
            ],
            kwargs={
                "c0": c0,
                "c1": c1,
                "c2": c2,
                "c3": c3,
                "d": d,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def lut3d(
        self,
        *,
        file: str,
        clut: int | Literal["first", "all"] | DefaultStr = DefaultStr("all"),
        interp: int
        | Literal["nearest", "trilinear", "tetrahedral", "pyramid", "prism"]
        | DefaultStr = DefaultStr("tetrahedral"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.151 lut3d
        Apply a 3D LUT to an input video.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str file: Set the 3D LUT file name. Currently supported formats: ‘3dl’ AfterEffects ‘cube’ Iridas ‘dat’ DaVinci ‘m3d’ Pandora ‘csp’ cineSpace
        :param int clut: None
        :param int interp: Select interpolation mode. Available values are: ‘nearest’ Use values from the nearest defined point. ‘trilinear’ Interpolate values using the 8 points defining a cube. ‘tetrahedral’ Interpolate values using a tetrahedron. ‘pyramid’ Interpolate values using a pyramid. ‘prism’ Interpolate values using a prism.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lut3d

        """
        filter_node = FilterNode(
            name="lut3d",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "file": file,
                "clut": clut,
                "interp": interp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def lutrgb(
        self,
        *,
        c0: str | DefaultStr = DefaultStr("clipval"),
        c1: str | DefaultStr = DefaultStr("clipval"),
        c2: str | DefaultStr = DefaultStr("clipval"),
        c3: str | DefaultStr = DefaultStr("clipval"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.153 lut, lutrgb, lutyuv
        Compute a look-up table for binding each pixel component input value
        to an output value, and apply it to the input video.

        lutyuv applies a lookup table to a YUV input video, lutrgb
        to an RGB input video.

        These filters accept the following parameters:

        Each of them specifies the expression to use for computing the lookup table for
        the corresponding pixel component values.

        The exact component associated to each of the c* options depends on the
        format in input.

        The lut filter requires either YUV or RGB pixel formats in input,
        lutrgb requires RGB pixel formats in input, and lutyuv requires YUV.

        The expressions can contain the following constants and functions:


        All expressions default to "clipval".

        Parameters:
        ----------

        :param str c0: set first pixel component expression
        :param str c1: set second pixel component expression
        :param str c2: set third pixel component expression
        :param str c3: set fourth pixel component expression, corresponds to the alpha component

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lut_002c-lutrgb_002c-lutyuv

        """
        filter_node = FilterNode(
            name="lutrgb",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "c0": c0,
                "c1": c1,
                "c2": c2,
                "c3": c3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def lutyuv(
        self,
        *,
        c0: str | DefaultStr = DefaultStr("clipval"),
        c1: str | DefaultStr = DefaultStr("clipval"),
        c2: str | DefaultStr = DefaultStr("clipval"),
        c3: str | DefaultStr = DefaultStr("clipval"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.153 lut, lutrgb, lutyuv
        Compute a look-up table for binding each pixel component input value
        to an output value, and apply it to the input video.

        lutyuv applies a lookup table to a YUV input video, lutrgb
        to an RGB input video.

        These filters accept the following parameters:

        Each of them specifies the expression to use for computing the lookup table for
        the corresponding pixel component values.

        The exact component associated to each of the c* options depends on the
        format in input.

        The lut filter requires either YUV or RGB pixel formats in input,
        lutrgb requires RGB pixel formats in input, and lutyuv requires YUV.

        The expressions can contain the following constants and functions:


        All expressions default to "clipval".

        Parameters:
        ----------

        :param str c0: set first pixel component expression
        :param str c1: set second pixel component expression
        :param str c2: set third pixel component expression
        :param str c3: set fourth pixel component expression, corresponds to the alpha component

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lut_002c-lutrgb_002c-lutyuv

        """
        filter_node = FilterNode(
            name="lutyuv",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "c0": c0,
                "c1": c1,
                "c2": c2,
                "c3": c3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def maskedclamp(
        self,
        _dark: "VideoStream",
        _bright: "VideoStream",
        *,
        undershoot: int | DefaultInt = DefaultInt(0),
        overshoot: int | DefaultInt = DefaultInt(0),
        planes: int | DefaultStr = DefaultStr("0xF"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.155 maskedclamp
        Clamp the first input stream with the second input and third input stream.

        Returns the value of first stream to be between second input
        stream - undershoot and third input stream + overshoot.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int undershoot: Default value is 0.
        :param int overshoot: Default value is 0.
        :param int planes: Set which planes will be processed as bitmap, unprocessed planes will be copied from first stream. By default value 0xf, all planes will be processed.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#maskedclamp

        """
        filter_node = FilterNode(
            name="maskedclamp",
            input_typings=[StreamType.video, StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _dark,
                _bright,
            ],
            kwargs={
                "undershoot": undershoot,
                "overshoot": overshoot,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def maskedmax(
        self,
        _filter1: "VideoStream",
        _filter2: "VideoStream",
        *,
        planes: int | DefaultStr = DefaultStr("0xF"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.156 maskedmax
        Merge the second and third input stream into output stream using absolute differences
        between second input stream and first input stream and absolute difference between
        third input stream and first input stream. The picked value will be from second input
        stream if second absolute difference is greater than first one or from third input stream
        otherwise.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int planes: Set which planes will be processed as bitmap, unprocessed planes will be copied from first stream. By default value 0xf, all planes will be processed.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#maskedmax

        """
        filter_node = FilterNode(
            name="maskedmax",
            input_typings=[StreamType.video, StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _filter1,
                _filter2,
            ],
            kwargs={
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def maskedmerge(
        self,
        _overlay: "VideoStream",
        _mask: "VideoStream",
        *,
        planes: int | DefaultStr = DefaultStr("0xF"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.157 maskedmerge
        Merge the first input stream with the second input stream using per pixel
        weights in the third input stream.

        A value of 0 in the third stream pixel component means that pixel component
        from first stream is returned unchanged, while maximum value (eg. 255 for
        8-bit videos) means that pixel component from second stream is returned
        unchanged. Intermediate values define the amount of merging between both
        input stream’s pixel components.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int planes: Set which planes will be processed as bitmap, unprocessed planes will be copied from first stream. By default value 0xf, all planes will be processed.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#maskedmerge

        """
        filter_node = FilterNode(
            name="maskedmerge",
            input_typings=[StreamType.video, StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _overlay,
                _mask,
            ],
            kwargs={
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def maskedmin(
        self,
        _filter1: "VideoStream",
        _filter2: "VideoStream",
        *,
        planes: int | DefaultStr = DefaultStr("0xF"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.158 maskedmin
        Merge the second and third input stream into output stream using absolute differences
        between second input stream and first input stream and absolute difference between
        third input stream and first input stream. The picked value will be from second input
        stream if second absolute difference is less than first one or from third input stream
        otherwise.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int planes: Set which planes will be processed as bitmap, unprocessed planes will be copied from first stream. By default value 0xf, all planes will be processed.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#maskedmin

        """
        filter_node = FilterNode(
            name="maskedmin",
            input_typings=[StreamType.video, StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _filter1,
                _filter2,
            ],
            kwargs={
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def maskedthreshold(
        self,
        _reference: "VideoStream",
        *,
        threshold: int | DefaultInt = DefaultInt(1),
        planes: int | DefaultStr = DefaultStr("0xF"),
        mode: int | Literal["abs", "diff"] | DefaultStr = DefaultStr("abs"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.159 maskedthreshold
        Pick pixels comparing absolute difference of two video streams with fixed
        threshold.

        If absolute difference between pixel component of first and second video
        stream is equal or lower than user supplied threshold than pixel component
        from first video stream is picked, otherwise pixel component from second
        video stream is picked.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int threshold: Set threshold used when picking pixels from absolute difference from two input video streams.
        :param int planes: Set which planes will be processed as bitmap, unprocessed planes will be copied from second stream. By default value 0xf, all planes will be processed.
        :param int mode: Set mode of filter operation. Can be abs or diff. Default is abs.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#maskedthreshold

        """
        filter_node = FilterNode(
            name="maskedthreshold",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _reference,
            ],
            kwargs={
                "threshold": threshold,
                "planes": planes,
                "mode": mode,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def maskfun(
        self,
        *,
        low: int | DefaultInt = DefaultInt(10),
        high: int | DefaultInt = DefaultInt(10),
        planes: int | DefaultStr = DefaultStr("0xF"),
        fill: int | DefaultInt = DefaultInt(0),
        sum: int | DefaultInt = DefaultInt(10),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.160 maskfun
        Create mask from input video.

        For example it is useful to create motion masks after tblend filter.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int low: Set low threshold. Any pixel component lower or exact than this value will be set to 0.
        :param int high: Set high threshold. Any pixel component higher than this value will be set to max value allowed for current pixel format.
        :param int planes: Set planes to filter, by default all available planes are filtered.
        :param int fill: Fill all frame pixels with this value.
        :param int sum: Set max average pixel value for frame. If sum of all pixel components is higher that this average, output frame will be completely filled with value set by fill option. Typically useful for scene changes when used in combination with tblend filter.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#maskfun

        """
        filter_node = FilterNode(
            name="maskfun",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "low": low,
                "high": high,
                "planes": planes,
                "fill": fill,
                "sum": sum,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def mcdeint(
        self,
        *,
        mode: int | DefaultStr = DefaultStr("MODE_FAST"),
        parity: int | Literal["tff", "bff"] | DefaultStr = DefaultStr("bff"),
        qp: int | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.161 mcdeint
        Apply motion-compensation deinterlacing.

        It needs one field per frame as input and must thus be used together
        with yadif=1/3 or equivalent.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int mode: Set the deinterlacing mode. It accepts one of the following values: ‘fast’ ‘medium’ ‘slow’ use iterative motion estimation ‘extra_slow’ like ‘slow’, but use multiple reference frames. Default value is ‘fast’.
        :param int parity: Set the picture field parity assumed for the input video. It must be one of the following values: ‘0, tff’ assume top field first ‘1, bff’ assume bottom field first Default value is ‘bff’.
        :param int qp: Set per-block quantization parameter (QP) used by the internal encoder. Higher values should result in a smoother motion vector field but less optimal individual vectors. Default value is 1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#mcdeint

        """
        filter_node = FilterNode(
            name="mcdeint",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "parity": parity,
                "qp": qp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def median(
        self,
        *,
        radius: int | DefaultInt = DefaultInt(1),
        planes: int | DefaultStr = DefaultStr("0xF"),
        radiusV: int | DefaultInt = DefaultInt(0),
        percentile: float | DefaultFloat = DefaultFloat(0.5),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.162 median
        Pick median pixel from certain rectangle defined by radius.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int radius: Set horizontal radius size. Default value is 1. Allowed range is integer from 1 to 127.
        :param int planes: Set which planes to process. Default is 15, which is all available planes.
        :param int radiusV: Set vertical radius size. Default value is 0. Allowed range is integer from 0 to 127. If it is 0, value will be picked from horizontal radius option.
        :param float percentile: Set median percentile. Default value is 0.5. Default value of 0.5 will pick always median values, while 0 will pick minimum values, and 1 maximum values.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#median

        """
        filter_node = FilterNode(
            name="median",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "radius": radius,
                "planes": planes,
                "radiusV": radiusV,
                "percentile": percentile,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def mestimate(
        self,
        *,
        method: int
        | Literal["esa", "tss", "tdls", "ntss", "fss", "ds", "hexbs", "epzs", "umh"]
        | DefaultStr = DefaultStr("esa"),
        mb_size: int | DefaultInt = DefaultInt(16),
        search_param: int | DefaultInt = DefaultInt(7),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.164 mestimate
        Estimate and export motion vectors using block matching algorithms.
        Motion vectors are stored in frame side data to be used by other filters.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int method: Specify the motion estimation method. Accepts one of the following values: ‘esa’ Exhaustive search algorithm. ‘tss’ Three step search algorithm. ‘tdls’ Two dimensional logarithmic search algorithm. ‘ntss’ New three step search algorithm. ‘fss’ Four step search algorithm. ‘ds’ Diamond search algorithm. ‘hexbs’ Hexagon-based search algorithm. ‘epzs’ Enhanced predictive zonal search algorithm. ‘umh’ Uneven multi-hexagon search algorithm. Default value is ‘esa’.
        :param int mb_size: Macroblock size. Default 16.
        :param int search_param: Search parameter. Default 7.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#mestimate

        """
        filter_node = FilterNode(
            name="mestimate",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "method": method,
                "mb_size": mb_size,
                "search_param": search_param,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def metadata(
        self,
        *,
        mode: int | Literal["select", "add", "modify", "delete", "print"] | DefaultStr = DefaultStr(0),
        key: str,
        value: str,
        function: int
        | Literal["same_str", "starts_with", "less", "equal", "greater", "expr", "ends_with"]
        | DefaultStr = DefaultStr(0),
        expr: str,
        file: str,
        direct: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        18.13 metadata, ametadata
        Manipulate frame metadata.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int mode: Set mode of operation of the filter. Can be one of the following: ‘select’ If both value and key is set, select frames which have such metadata. If only key is set, select every frame that has such key in metadata. ‘add’ Add new metadata key and value. If key is already available do nothing. ‘modify’ Modify value of already present key. ‘delete’ If value is set, delete only keys that have such value. Otherwise, delete key. If key is not set, delete all metadata values in the frame. ‘print’ Print key and its value if metadata was found. If key is not set print all metadata values available in frame.
        :param str key: Set key used with all modes. Must be set for all modes except print and delete.
        :param str value: Set metadata value which will be used. This option is mandatory for modify and add mode.
        :param int function: Which function to use when comparing metadata value and value. Can be one of following: ‘same_str’ Values are interpreted as strings, returns true if metadata value is same as value. ‘starts_with’ Values are interpreted as strings, returns true if metadata value starts with the value option string. ‘less’ Values are interpreted as floats, returns true if metadata value is less than value. ‘equal’ Values are interpreted as floats, returns true if value is equal with metadata value. ‘greater’ Values are interpreted as floats, returns true if metadata value is greater than value. ‘expr’ Values are interpreted as floats, returns true if expression from option expr evaluates to true. ‘ends_with’ Values are interpreted as strings, returns true if metadata value ends with the value option string.
        :param str expr: Set expression which is used when function is set to expr. The expression is evaluated through the eval API and can contain the following constants: VALUE1, FRAMEVAL Float representation of value from metadata key. VALUE2, USERVAL Float representation of value as supplied by user in value option.
        :param str file: If specified in print mode, output is written to the named file. Instead of plain filename any writable url can be specified. Filename “-” is a shorthand for standard output. If file option is not set, output is written to the log with AV_LOG_INFO loglevel.
        :param bool direct: Reduces buffering in print mode when output is written to a URL set using file.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#metadata_002c-ametadata

        """
        filter_node = FilterNode(
            name="metadata",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "key": key,
                "value": value,
                "function": function,
                "expr": expr,
                "file": file,
                "direct": direct,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def midequalizer(
        self, _in1: "VideoStream", *, planes: int | DefaultStr = DefaultStr("0xF"), **kwargs: Any
    ) -> "VideoStream":
        """

        11.165 midequalizer
        Apply Midway Image Equalization effect using two video streams.

        Midway Image Equalization adjusts a pair of images to have the same
        histogram, while maintaining their dynamics as much as possible. It’s
        useful for e.g. matching exposures from a pair of stereo cameras.

        This filter has two inputs and one output, which must be of same pixel format, but
        may be of different sizes. The output of filter is first input adjusted with
        midway histogram of both inputs.

        This filter accepts the following option:

        Parameters:
        ----------

        :param int planes: Set which planes to process. Default is 15, which is all available planes.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#midequalizer

        """
        filter_node = FilterNode(
            name="midequalizer",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _in1,
            ],
            kwargs={
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def minterpolate(
        self,
        *,
        fps: str | DefaultStr = DefaultStr("60"),
        mi_mode: int | Literal["dup", "blend", "mci"] | DefaultStr = DefaultStr("mci"),
        mc_mode: int | Literal["obmc", "aobmc"] | DefaultStr = DefaultStr("obmc"),
        me_mode: int | Literal["bidir", "bilat"] | DefaultStr = DefaultStr("bilat"),
        me: int
        | Literal["esa", "tss", "tdls", "ntss", "fss", "ds", "hexbs", "epzs", "umh"]
        | DefaultStr = DefaultStr("epzs"),
        mb_size: int | DefaultInt = DefaultInt(16),
        search_param: int | DefaultInt = DefaultInt(32),
        vsbmc: int | DefaultInt = DefaultInt(0),
        scd: int | Literal["none", "fdiff"] | DefaultStr = DefaultStr("fdiff"),
        scd_threshold: float | DefaultFloat = DefaultFloat(10.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.166 minterpolate
        Convert the video to specified frame rate using motion interpolation.

        This filter accepts the following options:

        Parameters:
        ----------

        :param str fps: Specify the output frame rate. This can be rational e.g. 60000/1001. Frames are dropped if fps is lower than source fps. Default 60.
        :param int mi_mode: Motion interpolation mode. Following values are accepted: ‘dup’ Duplicate previous or next frame for interpolating new ones. ‘blend’ Blend source frames. Interpolated frame is mean of previous and next frames. ‘mci’ Motion compensated interpolation. Following options are effective when this mode is selected: ‘mc_mode’ Motion compensation mode. Following values are accepted: ‘obmc’ Overlapped block motion compensation. ‘aobmc’ Adaptive overlapped block motion compensation. Window weighting coefficients are controlled adaptively according to the reliabilities of the neighboring motion vectors to reduce oversmoothing. Default mode is ‘obmc’. ‘me_mode’ Motion estimation mode. Following values are accepted: ‘bidir’ Bidirectional motion estimation. Motion vectors are estimated for each source frame in both forward and backward directions. ‘bilat’ Bilateral motion estimation. Motion vectors are estimated directly for interpolated frame. Default mode is ‘bilat’. ‘me’ The algorithm to be used for motion estimation. Following values are accepted: ‘esa’ Exhaustive search algorithm. ‘tss’ Three step search algorithm. ‘tdls’ Two dimensional logarithmic search algorithm. ‘ntss’ New three step search algorithm. ‘fss’ Four step search algorithm. ‘ds’ Diamond search algorithm. ‘hexbs’ Hexagon-based search algorithm. ‘epzs’ Enhanced predictive zonal search algorithm. ‘umh’ Uneven multi-hexagon search algorithm. Default algorithm is ‘epzs’. ‘mb_size’ Macroblock size. Default 16. ‘search_param’ Motion estimation search parameter. Default 32. ‘vsbmc’ Enable variable-size block motion compensation. Motion estimation is applied with smaller block sizes at object boundaries in order to make the them less blur. Default is 0 (disabled).
        :param int mc_mode: None
        :param int me_mode: None
        :param int me: None
        :param int mb_size: None
        :param int search_param: None
        :param int vsbmc: None
        :param int scd: Scene change detection method. Scene change leads motion vectors to be in random direction. Scene change detection replace interpolated frames by duplicate ones. May not be needed for other modes. Following values are accepted: ‘none’ Disable scene change detection. ‘fdiff’ Frame difference. Corresponding pixel values are compared and if it satisfies scd_threshold scene change is detected. Default method is ‘fdiff’.
        :param float scd_threshold: Scene change detection threshold. Default is 10..

        Ref: https://ffmpeg.org/ffmpeg-filters.html#minterpolate

        """
        filter_node = FilterNode(
            name="minterpolate",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "fps": fps,
                "mi_mode": mi_mode,
                "mc_mode": mc_mode,
                "me_mode": me_mode,
                "me": me,
                "mb_size": mb_size,
                "search_param": search_param,
                "vsbmc": vsbmc,
                "scd": scd,
                "scd_threshold": scd_threshold,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def monochrome(
        self,
        *,
        cb: float | DefaultFloat = DefaultFloat(0.0),
        cr: float | DefaultFloat = DefaultFloat(0.0),
        size: float | DefaultFloat = DefaultFloat(1.0),
        high: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.168 monochrome
        Convert video to gray using custom color filter.

        A description of the accepted options follows.

        Parameters:
        ----------

        :param float cb: Set the chroma blue spot. Allowed range is from -1 to 1. Default value is 0.
        :param float cr: Set the chroma red spot. Allowed range is from -1 to 1. Default value is 0.
        :param float size: Set the color filter size. Allowed range is from .1 to 10. Default value is 1.
        :param float high: Set the highlights strength. Allowed range is from 0 to 1. Default value is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#monochrome

        """
        filter_node = FilterNode(
            name="monochrome",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "cb": cb,
                "cr": cr,
                "size": size,
                "high": high,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def morpho(
        self,
        _structure: "VideoStream",
        *,
        mode: int
        | Literal["erode", "dilate", "open", "close", "gradient", "tophat", "blackhat"]
        | DefaultStr = DefaultStr(0),
        planes: int | DefaultInt = DefaultInt(7),
        structure: int | Literal["first", "all"] | DefaultStr = DefaultStr("all"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.169 morpho
        This filter allows to apply main morphological grayscale transforms,
        erode and dilate with arbitrary structures set in second input stream.

        Unlike naive implementation and much slower performance in erosion
        and dilation filters, when speed is critical morpho filter
        should be used instead.

        A description of accepted options follows,


        The morpho filter also supports the framesync options.

        Parameters:
        ----------

        :param int mode: Set morphological transform to apply, can be: ‘erode’ ‘dilate’ ‘open’ ‘close’ ‘gradient’ ‘tophat’ ‘blackhat’ Default is erode.
        :param int planes: Set planes to filter, by default all planes except alpha are filtered.
        :param int structure: Set which structure video frames will be processed from second input stream, can be first or all. Default is all.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#morpho

        """
        filter_node = FilterNode(
            name="morpho",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _structure,
            ],
            kwargs={
                "mode": mode,
                "planes": planes,
                "structure": structure,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def mpdecimate(
        self,
        *,
        max: int | DefaultInt = DefaultInt(0),
        keep: int | DefaultInt = DefaultInt(0),
        hi: int | DefaultStr = DefaultStr("64*12"),
        lo: int | DefaultStr = DefaultStr("64*5"),
        frac: float | DefaultFloat = DefaultFloat(0.33),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.170 mpdecimate
        Drop frames that do not differ greatly from the previous frame in
        order to reduce frame rate.

        The main use of this filter is for very-low-bitrate encoding
        (e.g. streaming over dialup modem), but it could in theory be used for
        fixing movies that were inverse-telecined incorrectly.

        A description of the accepted options follows.

        Parameters:
        ----------

        :param int max: Set the maximum number of consecutive frames which can be dropped (if positive), or the minimum interval between dropped frames (if negative). If the value is 0, the frame is dropped disregarding the number of previous sequentially dropped frames. Default value is 0.
        :param int keep: Set the maximum number of consecutive similar frames to ignore before to start dropping them. If the value is 0, the frame is dropped disregarding the number of previous sequentially similar frames. Default value is 0.
        :param int hi: Set the dropping threshold values. Values for hi and lo are for 8x8 pixel blocks and represent actual pixel value differences, so a threshold of 64 corresponds to 1 unit of difference for each pixel, or the same spread out differently over the block. A frame is a candidate for dropping if no 8x8 blocks differ by more than a threshold of hi, and if no more than frac blocks (1 meaning the whole image) differ by more than a threshold of lo. Default value for hi is 64*12, default value for lo is 64*5, and default value for frac is 0.33.
        :param int lo: Set the dropping threshold values. Values for hi and lo are for 8x8 pixel blocks and represent actual pixel value differences, so a threshold of 64 corresponds to 1 unit of difference for each pixel, or the same spread out differently over the block. A frame is a candidate for dropping if no 8x8 blocks differ by more than a threshold of hi, and if no more than frac blocks (1 meaning the whole image) differ by more than a threshold of lo. Default value for hi is 64*12, default value for lo is 64*5, and default value for frac is 0.33.
        :param float frac: Set the dropping threshold values. Values for hi and lo are for 8x8 pixel blocks and represent actual pixel value differences, so a threshold of 64 corresponds to 1 unit of difference for each pixel, or the same spread out differently over the block. A frame is a candidate for dropping if no 8x8 blocks differ by more than a threshold of hi, and if no more than frac blocks (1 meaning the whole image) differ by more than a threshold of lo. Default value for hi is 64*12, default value for lo is 64*5, and default value for frac is 0.33.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#mpdecimate

        """
        filter_node = FilterNode(
            name="mpdecimate",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "max": max,
                "keep": keep,
                "hi": hi,
                "lo": lo,
                "frac": frac,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def msad(self, _reference: "VideoStream", **kwargs: Any) -> "VideoStream":
        """

        11.171 msad
        Obtain the MSAD (Mean Sum of Absolute Differences) between two input videos.

        This filter takes two input videos.

        Both input videos must have the same resolution and pixel format for
        this filter to work correctly. Also it assumes that both inputs
        have the same number of frames, which are compared one by one.

        The obtained per component, average, min and max MSAD is printed through
        the logging system.

        The filter stores the calculated MSAD of each frame in frame metadata.

        This filter also supports the framesync options.

        In the below example the input file main.mpg being processed is compared
        with the reference file ref.mpg.


        ffmpeg -i main.mpg -i ref.mpg -lavfi msad -f null -

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#msad

        """
        filter_node = FilterNode(
            name="msad",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _reference,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def multiply(
        self,
        _factor: "VideoStream",
        *,
        scale: float | DefaultFloat = DefaultFloat(1.0),
        offset: float | DefaultFloat = DefaultFloat(0.5),
        planes: str | DefaultStr = DefaultStr("0xF"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.172 multiply
        Multiply first video stream pixels values with second video stream pixels values.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float scale: Set the scale applied to second video stream. By default is 1. Allowed range is from 0 to 9.
        :param float offset: Set the offset applied to second video stream. By default is 0.5. Allowed range is from -1 to 1.
        :param str planes: Specify planes from input video stream that will be processed. By default all planes are processed.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#multiply

        """
        filter_node = FilterNode(
            name="multiply",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _factor,
            ],
            kwargs={
                "scale": scale,
                "offset": offset,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def negate(
        self,
        *,
        components: str | Literal["y", "u", "v", "r", "g", "b", "a"] | DefaultStr = DefaultStr("0x77"),
        negate_alpha: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.173 negate
        Negate (invert) the input video.

        It accepts the following option:

        Parameters:
        ----------

        :param str components: Set components to negate. Available values for components are: ‘y’ ‘u’ ‘v’ ‘a’ ‘r’ ‘g’ ‘b’
        :param bool negate_alpha: With value 1, it negates the alpha component, if present. Default value is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#negate

        """
        filter_node = FilterNode(
            name="negate",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "components": components,
                "negate_alpha": negate_alpha,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def nlmeans(
        self,
        *,
        s: float | DefaultFloat = DefaultFloat(1.0),
        p: int | DefaultStr = DefaultStr("3*2+1"),
        pc: int | DefaultInt = DefaultInt(0),
        r: int | DefaultStr = DefaultStr("7*2+1"),
        rc: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.174 nlmeans
        Denoise frames using Non-Local Means algorithm.

        Each pixel is adjusted by looking for other pixels with similar contexts. This
        context similarity is defined by comparing their surrounding patches of size
        pxp. Patches are searched in an area of rxr
        around the pixel.

        Note that the research area defines centers for patches, which means some
        patches will be made of pixels outside that research area.

        The filter accepts the following options.

        Parameters:
        ----------

        :param float s: Set denoising strength. Default is 1.0. Must be in range [1.0, 30.0].
        :param int p: Set patch size. Default is 7. Must be odd number in range [0, 99].
        :param int pc: Same as p but for chroma planes. The default value is 0 and means automatic.
        :param int r: Set research size. Default is 15. Must be odd number in range [0, 99].
        :param int rc: Same as r but for chroma planes. The default value is 0 and means automatic.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#nlmeans

        """
        filter_node = FilterNode(
            name="nlmeans",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "s": s,
                "p": p,
                "pc": pc,
                "r": r,
                "rc": rc,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def nlmeans_opencl(
        self,
        *,
        s: float | DefaultFloat = DefaultFloat(1.0),
        p: int | DefaultStr = DefaultStr("2*3+1"),
        pc: int | DefaultInt = DefaultInt(0),
        r: int | DefaultStr = DefaultStr("7*2+1"),
        rc: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.8 nlmeans_opencl
        Non-local Means denoise filter through OpenCL, this filter accepts same options as nlmeans.

        Parameters:
        ----------

        :param float s: None
        :param int p: None
        :param int pc: None
        :param int r: None
        :param int rc: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#nlmeans_005fopencl

        """
        filter_node = FilterNode(
            name="nlmeans_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "s": s,
                "p": p,
                "pc": pc,
                "r": r,
                "rc": rc,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def nlmeans_vulkan(
        self,
        *,
        s: float | DefaultFloat = DefaultFloat(1.0),
        p: int | DefaultStr = DefaultStr("3*2+1"),
        r: int | DefaultStr = DefaultStr("7*2+1"),
        t: int | DefaultInt = DefaultInt(36),
        s1: float | DefaultFloat = DefaultFloat(1.0),
        s2: float | DefaultFloat = DefaultFloat(1.0),
        s3: float | DefaultFloat = DefaultFloat(1.0),
        s4: float | DefaultFloat = DefaultFloat(1.0),
        p1: int | DefaultInt = DefaultInt(0),
        p2: int | DefaultInt = DefaultInt(0),
        p3: int | DefaultInt = DefaultInt(0),
        p4: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        14.10 nlmeans_vulkan
        Denoise frames using Non-Local Means algorithm, implemented on the GPU using
        Vulkan.
        Supports more pixel formats than nlmeans or nlmeans_opencl, including
        alpha channel support.

        The filter accepts the following options.

        Parameters:
        ----------

        :param float s: Set denoising strength for all components. Default is 1.0. Must be in range [1.0, 100.0].
        :param int p: Set patch size for all planes. Default is 7. Must be odd number in range [0, 99].
        :param int r: Set research size. Default is 15. Must be odd number in range [0, 99].
        :param int t: Set parallelism. Default is 36. Must be a number in the range [1, 168]. Larger values may speed up processing, at the cost of more VRAM. Lower values will slow it down, reducing VRAM usage. Only supported on GPUs with atomic float operations (RDNA3+, Ampere+).
        :param float s1: Set denoising strength for a specific component. Default is 1, equal to s. Must be odd number in range [1, 100].
        :param float s2: Set denoising strength for a specific component. Default is 1, equal to s. Must be odd number in range [1, 100].
        :param float s3: Set denoising strength for a specific component. Default is 1, equal to s. Must be odd number in range [1, 100].
        :param float s4: None
        :param int p1: Set patch size for a specific component. Default is 7, equal to p. Must be odd number in range [0, 99].
        :param int p2: Set patch size for a specific component. Default is 7, equal to p. Must be odd number in range [0, 99].
        :param int p3: Set patch size for a specific component. Default is 7, equal to p. Must be odd number in range [0, 99].
        :param int p4: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#nlmeans_005fvulkan

        """
        filter_node = FilterNode(
            name="nlmeans_vulkan",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "s": s,
                "p": p,
                "r": r,
                "t": t,
                "s1": s1,
                "s2": s2,
                "s3": s3,
                "s4": s4,
                "p1": p1,
                "p2": p2,
                "p3": p3,
                "p4": p4,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def nnedi(
        self,
        *,
        weights: str | DefaultStr = DefaultStr("nnedi3_weights.bin"),
        deint: int | Literal["all", "interlaced"] | DefaultStr = DefaultStr("all"),
        field: int | Literal["af", "a", "t", "b", "tf", "bf"] | DefaultStr = DefaultStr("a"),
        planes: int | DefaultInt = DefaultInt(7),
        nsize: int
        | Literal["s8x6", "s16x6", "s32x6", "s48x6", "s8x4", "s16x4", "s32x4"]
        | DefaultStr = DefaultStr("s32x4"),
        nns: int | Literal["n16", "n32", "n64", "n128", "n256"] | DefaultStr = DefaultStr("n32"),
        qual: int | Literal["fast", "slow"] | DefaultStr = DefaultStr("fast"),
        etype: int | Literal["a", "abs", "s", "mse"] | DefaultStr = DefaultStr("a"),
        pscrn: int | Literal["none", "original", "new", "new2", "new3"] | DefaultStr = DefaultStr("new"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.175 nnedi
        Deinterlace video using neural network edge directed interpolation.

        This filter accepts the following options:

        Parameters:
        ----------

        :param str weights: Mandatory option, without binary file filter can not work. Currently file can be found here: https://github.com/dubhater/vapoursynth-nnedi3/blob/master/src/nnedi3_weights.bin
        :param int deint: Set which frames to deinterlace, by default it is all. Can be all or interlaced.
        :param int field: Set mode of operation. Can be one of the following: ‘af’ Use frame flags, both fields. ‘a’ Use frame flags, single field. ‘t’ Use top field only. ‘b’ Use bottom field only. ‘tf’ Use both fields, top first. ‘bf’ Use both fields, bottom first.
        :param int planes: Set which planes to process, by default filter process all frames.
        :param int nsize: Set size of local neighborhood around each pixel, used by the predictor neural network. Can be one of the following: ‘s8x6’ ‘s16x6’ ‘s32x6’ ‘s48x6’ ‘s8x4’ ‘s16x4’ ‘s32x4’
        :param int nns: Set the number of neurons in predictor neural network. Can be one of the following: ‘n16’ ‘n32’ ‘n64’ ‘n128’ ‘n256’
        :param int qual: Controls the number of different neural network predictions that are blended together to compute the final output value. Can be fast, default or slow.
        :param int etype: Set which set of weights to use in the predictor. Can be one of the following: ‘a, abs’ weights trained to minimize absolute error ‘s, mse’ weights trained to minimize squared error
        :param int pscrn: Controls whether or not the prescreener neural network is used to decide which pixels should be processed by the predictor neural network and which can be handled by simple cubic interpolation. The prescreener is trained to know whether cubic interpolation will be sufficient for a pixel or whether it should be predicted by the predictor nn. The computational complexity of the prescreener nn is much less than that of the predictor nn. Since most pixels can be handled by cubic interpolation, using the prescreener generally results in much faster processing. The prescreener is pretty accurate, so the difference between using it and not using it is almost always unnoticeable. Can be one of the following: ‘none’ ‘original’ ‘new’ ‘new2’ ‘new3’ Default is new.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#nnedi

        """
        filter_node = FilterNode(
            name="nnedi",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "weights": weights,
                "deint": deint,
                "field": field,
                "planes": planes,
                "nsize": nsize,
                "nns": nns,
                "qual": qual,
                "etype": etype,
                "pscrn": pscrn,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def noformat(self, *, pix_fmts: str, **kwargs: Any) -> "VideoStream":
        """

        11.176 noformat
        Force libavfilter not to use any of the specified pixel formats for the
        input to the next filter.

        It accepts the following parameters:

        Parameters:
        ----------

        :param str pix_fmts: A ’|’-separated list of pixel format names, such as pix_fmts=yuv420p|monow|rgb24".

        Ref: https://ffmpeg.org/ffmpeg-filters.html#noformat

        """
        filter_node = FilterNode(
            name="noformat",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "pix_fmts": pix_fmts,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def noise(
        self,
        *,
        all_seed: int | DefaultInt = DefaultInt(-1),
        all_strength: int | DefaultInt = DefaultInt(0),
        all_flags: str | Literal["a", "p", "t", "u"] | DefaultStr = DefaultStr(0),
        c0_seed: int | DefaultInt = DefaultInt(-1),
        c0_strength: int | DefaultInt = DefaultInt(0),
        c0_flags: str | Literal["a", "p", "t", "u"] | DefaultStr = DefaultStr(0),
        c1_seed: int | DefaultInt = DefaultInt(-1),
        c1_strength: int | DefaultInt = DefaultInt(0),
        c1_flags: str | Literal["a", "p", "t", "u"] | DefaultStr = DefaultStr(0),
        c2_seed: int | DefaultInt = DefaultInt(-1),
        c2_strength: int | DefaultInt = DefaultInt(0),
        c2_flags: str | Literal["a", "p", "t", "u"] | DefaultStr = DefaultStr(0),
        c3_seed: int | DefaultInt = DefaultInt(-1),
        c3_strength: int | DefaultInt = DefaultInt(0),
        c3_flags: str | Literal["a", "p", "t", "u"] | DefaultStr = DefaultStr(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.177 noise
        Add noise on video input frame.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int all_seed: Set noise seed for specific pixel component or all pixel components in case of all_seed. Default value is 123457.
        :param int all_strength: Set noise strength for specific pixel component or all pixel components in case all_strength. Default value is 0. Allowed range is [0, 100].
        :param str all_flags: Set pixel component flags or set flags for all components if all_flags. Available values for component flags are: ‘a’ averaged temporal noise (smoother) ‘p’ mix random noise with a (semi)regular pattern ‘t’ temporal noise (noise pattern changes between frames) ‘u’ uniform noise (gaussian otherwise)
        :param int c0_seed: Set noise seed for specific pixel component or all pixel components in case of all_seed. Default value is 123457.
        :param int c0_strength: Set noise strength for specific pixel component or all pixel components in case all_strength. Default value is 0. Allowed range is [0, 100].
        :param str c0_flags: Set pixel component flags or set flags for all components if all_flags. Available values for component flags are: ‘a’ averaged temporal noise (smoother) ‘p’ mix random noise with a (semi)regular pattern ‘t’ temporal noise (noise pattern changes between frames) ‘u’ uniform noise (gaussian otherwise)
        :param int c1_seed: Set noise seed for specific pixel component or all pixel components in case of all_seed. Default value is 123457.
        :param int c1_strength: Set noise strength for specific pixel component or all pixel components in case all_strength. Default value is 0. Allowed range is [0, 100].
        :param str c1_flags: Set pixel component flags or set flags for all components if all_flags. Available values for component flags are: ‘a’ averaged temporal noise (smoother) ‘p’ mix random noise with a (semi)regular pattern ‘t’ temporal noise (noise pattern changes between frames) ‘u’ uniform noise (gaussian otherwise)
        :param int c2_seed: Set noise seed for specific pixel component or all pixel components in case of all_seed. Default value is 123457.
        :param int c2_strength: Set noise strength for specific pixel component or all pixel components in case all_strength. Default value is 0. Allowed range is [0, 100].
        :param str c2_flags: Set pixel component flags or set flags for all components if all_flags. Available values for component flags are: ‘a’ averaged temporal noise (smoother) ‘p’ mix random noise with a (semi)regular pattern ‘t’ temporal noise (noise pattern changes between frames) ‘u’ uniform noise (gaussian otherwise)
        :param int c3_seed: Set noise seed for specific pixel component or all pixel components in case of all_seed. Default value is 123457.
        :param int c3_strength: Set noise strength for specific pixel component or all pixel components in case all_strength. Default value is 0. Allowed range is [0, 100].
        :param str c3_flags: Set pixel component flags or set flags for all components if all_flags. Available values for component flags are: ‘a’ averaged temporal noise (smoother) ‘p’ mix random noise with a (semi)regular pattern ‘t’ temporal noise (noise pattern changes between frames) ‘u’ uniform noise (gaussian otherwise)

        Ref: https://ffmpeg.org/ffmpeg-filters.html#noise

        """
        filter_node = FilterNode(
            name="noise",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "all_seed": all_seed,
                "all_strength": all_strength,
                "all_flags": all_flags,
                "c0_seed": c0_seed,
                "c0_strength": c0_strength,
                "c0_flags": c0_flags,
                "c1_seed": c1_seed,
                "c1_strength": c1_strength,
                "c1_flags": c1_flags,
                "c2_seed": c2_seed,
                "c2_strength": c2_strength,
                "c2_flags": c2_flags,
                "c3_seed": c3_seed,
                "c3_strength": c3_strength,
                "c3_flags": c3_flags,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def normalize(
        self,
        *,
        blackpt: str | DefaultStr = DefaultStr("black"),
        whitept: str | DefaultStr = DefaultStr("white"),
        smoothing: int | DefaultInt = DefaultInt(0),
        independence: float | DefaultFloat = DefaultFloat(1.0),
        strength: float | DefaultFloat = DefaultFloat(1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.178 normalize
        Normalize RGB video (aka histogram stretching, contrast stretching).
        See: https://en.wikipedia.org/wiki/Normalization_(image_processing)

        For each channel of each frame, the filter computes the input range and maps
        it linearly to the user-specified output range. The output range defaults
        to the full dynamic range from pure black to pure white.

        Temporal smoothing can be used on the input range to reduce flickering (rapid
        changes in brightness) caused when small dark or bright objects enter or leave
        the scene. This is similar to the auto-exposure (automatic gain control) on a
        video camera, and, like a video camera, it may cause a period of over- or
        under-exposure of the video.

        The R,G,B channels can be normalized independently, which may cause some
        color shifting, or linked together as a single channel, which prevents
        color shifting. Linked normalization preserves hue. Independent normalization
        does not, so it can be used to remove some color casts. Independent and linked
        normalization can be combined in any ratio.

        The normalize filter accepts the following options:

        Parameters:
        ----------

        :param str blackpt: Colors which define the output range. The minimum input value is mapped to the blackpt. The maximum input value is mapped to the whitept. The defaults are black and white respectively. Specifying white for blackpt and black for whitept will give color-inverted, normalized video. Shades of grey can be used to reduce the dynamic range (contrast). Specifying saturated colors here can create some interesting effects.
        :param str whitept: Colors which define the output range. The minimum input value is mapped to the blackpt. The maximum input value is mapped to the whitept. The defaults are black and white respectively. Specifying white for blackpt and black for whitept will give color-inverted, normalized video. Shades of grey can be used to reduce the dynamic range (contrast). Specifying saturated colors here can create some interesting effects.
        :param int smoothing: The number of previous frames to use for temporal smoothing. The input range of each channel is smoothed using a rolling average over the current frame and the smoothing previous frames. The default is 0 (no temporal smoothing).
        :param float independence: Controls the ratio of independent (color shifting) channel normalization to linked (color preserving) normalization. 0.0 is fully linked, 1.0 is fully independent. Defaults to 1.0 (fully independent).
        :param float strength: Overall strength of the filter. 1.0 is full strength. 0.0 is a rather expensive no-op. Defaults to 1.0 (full strength).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#normalize

        """
        filter_node = FilterNode(
            name="normalize",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "blackpt": blackpt,
                "whitept": whitept,
                "smoothing": smoothing,
                "independence": independence,
                "strength": strength,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def null(self, **kwargs: Any) -> "VideoStream":
        """

        11.179 null
        Pass the video source unchanged to the output.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#null

        """
        filter_node = FilterNode(
            name="null",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def ocr(
        self,
        *,
        datapath: str,
        language: str | DefaultStr = DefaultStr("eng"),
        whitelist: str
        | DefaultStr = DefaultStr(
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.:;,-+_!?\\\\\"\\'[]{}()<>|/\\\\\\\\=*&%$#@!~ "
        ),
        blacklist: str | DefaultStr = DefaultStr(""),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.180 ocr
        Optical Character Recognition

        This filter uses Tesseract for optical character recognition. To enable
        compilation of this filter, you need to configure FFmpeg with
        --enable-libtesseract.

        It accepts the following options:


        The filter exports recognized text as the frame metadata lavfi.ocr.text.
        The filter exports confidence of recognized words as the frame metadata lavfi.ocr.confidence.

        Parameters:
        ----------

        :param str datapath: Set datapath to tesseract data. Default is to use whatever was set at installation.
        :param str language: Set language, default is "eng".
        :param str whitelist: Set character whitelist.
        :param str blacklist: Set character blacklist.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#ocr

        """
        filter_node = FilterNode(
            name="ocr",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "datapath": datapath,
                "language": language,
                "whitelist": whitelist,
                "blacklist": blacklist,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def ocv(self, *, filter_name: str, filter_params: str, **kwargs: Any) -> "VideoStream":
        """

        11.181 ocv
        Apply a video transform using libopencv.

        To enable this filter, install the libopencv library and headers and
        configure FFmpeg with --enable-libopencv.

        It accepts the following parameters:


        Refer to the official libopencv documentation for more precise
        information:
        http://docs.opencv.org/master/modules/imgproc/doc/filtering.html

        Several libopencv filters are supported; see the following subsections.

        Parameters:
        ----------

        :param str filter_name: The name of the libopencv filter to apply.
        :param str filter_params: The parameters to pass to the libopencv filter. If not specified, the default values are assumed.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#ocv

        """
        filter_node = FilterNode(
            name="ocv",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "filter_name": filter_name,
                "filter_params": filter_params,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def oscilloscope(
        self,
        *,
        x: float | DefaultFloat = DefaultFloat(0.5),
        y: float | DefaultFloat = DefaultFloat(0.5),
        s: float | DefaultFloat = DefaultFloat(0.8),
        t: float | DefaultFloat = DefaultFloat(0.5),
        o: float | DefaultFloat = DefaultFloat(0.8),
        tx: float | DefaultFloat = DefaultFloat(0.5),
        ty: float | DefaultFloat = DefaultFloat(0.9),
        tw: float | DefaultFloat = DefaultFloat(0.8),
        th: float | DefaultFloat = DefaultFloat(0.3),
        c: int | DefaultInt = DefaultInt(7),
        g: bool | DefaultInt = DefaultInt(1),
        st: bool | DefaultInt = DefaultInt(1),
        sc: bool | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.182 oscilloscope
        2D Video Oscilloscope.

        Useful to measure spatial impulse, step responses, chroma delays, etc.

        It accepts the following parameters:

        Parameters:
        ----------

        :param float x: Set scope center x position.
        :param float y: Set scope center y position.
        :param float s: Set scope size, relative to frame diagonal.
        :param float t: Set scope tilt/rotation.
        :param float o: Set trace opacity.
        :param float tx: Set trace center x position.
        :param float ty: Set trace center y position.
        :param float tw: Set trace width, relative to width of frame.
        :param float th: Set trace height, relative to height of frame.
        :param int c: Set which components to trace. By default it traces first three components.
        :param bool g: Draw trace grid. By default is enabled.
        :param bool st: Draw some statistics. By default is enabled.
        :param bool sc: Draw scope. By default is enabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#oscilloscope

        """
        filter_node = FilterNode(
            name="oscilloscope",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "x": x,
                "y": y,
                "s": s,
                "t": t,
                "o": o,
                "tx": tx,
                "ty": ty,
                "tw": tw,
                "th": th,
                "c": c,
                "g": g,
                "st": st,
                "sc": sc,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def overlay(
        self,
        _overlay: "VideoStream",
        *,
        x: str | DefaultStr = DefaultStr("0"),
        y: str | DefaultStr = DefaultStr("0"),
        eof_action: int | Literal["repeat", "endall", "pass"] | DefaultStr = DefaultStr("repeat"),
        eval: int | DefaultStr = DefaultStr("EVAL_MODE_FRAME"),
        shortest: bool | DefaultInt = DefaultInt(0),
        format: int | DefaultStr = DefaultStr("OVERLAY_FORMAT_YUV420"),
        repeatlast: bool | DefaultInt = DefaultInt(1),
        alpha: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.183 overlay
        Overlay one video on top of another.

        It takes two inputs and has one output. The first input is the "main"
        video on which the second input is overlaid.

        It accepts the following parameters:

        A description of the accepted options follows.


        The x, and y expressions can contain the following
        parameters.


        This filter also supports the framesync options.

        Note that the n, t variables are available only
        when evaluation is done per frame, and will evaluate to NAN
        when eval is set to ‘init’.

        Be aware that frames are taken from each input video in timestamp
        order, hence, if their initial timestamps differ, it is a good idea
        to pass the two inputs through a setpts=PTS-STARTPTS filter to
        have them begin in the same zero timestamp, as the example for
        the movie filter does.

        You can chain together more overlays but you should test the
        efficiency of such approach.

        Parameters:
        ----------

        :param str x: Set the expression for the x and y coordinates of the overlaid video on the main video. Default value is "0" for both expressions. In case the expression is invalid, it is set to a huge value (meaning that the overlay will not be displayed within the output visible area).
        :param str y: Set the expression for the x and y coordinates of the overlaid video on the main video. Default value is "0" for both expressions. In case the expression is invalid, it is set to a huge value (meaning that the overlay will not be displayed within the output visible area).
        :param int eof_action: See framesync.
        :param int eval: Set when the expressions for x, and y are evaluated. It accepts the following values: ‘init’ only evaluate expressions once during the filter initialization or when a command is processed ‘frame’ evaluate expressions for each incoming frame Default value is ‘frame’.
        :param bool shortest: See framesync.
        :param int format: Set the format for the output video. It accepts the following values: ‘yuv420’ force YUV 4:2:0 8-bit planar output ‘yuv420p10’ force YUV 4:2:0 10-bit planar output ‘yuv422’ force YUV 4:2:2 8-bit planar output ‘yuv422p10’ force YUV 4:2:2 10-bit planar output ‘yuv444’ force YUV 4:4:4 8-bit planar output ‘yuv444p10’ force YUV 4:4:4 10-bit planar output ‘rgb’ force RGB 8-bit packed output ‘gbrp’ force RGB 8-bit planar output ‘auto’ automatically pick format Default value is ‘yuv420’.
        :param bool repeatlast: See framesync.
        :param int alpha: Set format of alpha of the overlaid video, it can be straight or premultiplied. Default is straight.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#overlay

        """
        filter_node = FilterNode(
            name="overlay",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _overlay,
            ],
            kwargs={
                "x": x,
                "y": y,
                "eof_action": eof_action,
                "eval": eval,
                "shortest": shortest,
                "format": format,
                "repeatlast": repeatlast,
                "alpha": alpha,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def overlay_cuda(
        self,
        _overlay: "VideoStream",
        *,
        x: str | DefaultStr = DefaultStr("0"),
        y: str | DefaultStr = DefaultStr("0"),
        eof_action: int | Literal["repeat", "endall", "pass"] | DefaultStr = DefaultStr("repeat"),
        eval: int | DefaultStr = DefaultStr("EVAL_MODE_FRAME"),
        shortest: bool | DefaultInt = DefaultInt(0),
        repeatlast: bool | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.184 overlay_cuda
        Overlay one video on top of another.

        This is the CUDA variant of the overlay filter.
        It only accepts CUDA frames. The underlying input pixel formats have to match.

        It takes two inputs and has one output. The first input is the "main"
        video on which the second input is overlaid.

        It accepts the following parameters:


        This filter also supports the framesync options.

        Parameters:
        ----------

        :param str x: Set expressions for the x and y coordinates of the overlaid video on the main video. They can contain the following parameters: main_w, W main_h, H The main input width and height. overlay_w, w overlay_h, h The overlay input width and height. x y The computed values for x and y. They are evaluated for each new frame. n The ordinal index of the main input frame, starting from 0. pos The byte offset position in the file of the main input frame, NAN if unknown. Deprecated, do not use. t The timestamp of the main input frame, expressed in seconds, NAN if unknown. Default value is "0" for both expressions.
        :param str y: Set expressions for the x and y coordinates of the overlaid video on the main video. They can contain the following parameters: main_w, W main_h, H The main input width and height. overlay_w, w overlay_h, h The overlay input width and height. x y The computed values for x and y. They are evaluated for each new frame. n The ordinal index of the main input frame, starting from 0. pos The byte offset position in the file of the main input frame, NAN if unknown. Deprecated, do not use. t The timestamp of the main input frame, expressed in seconds, NAN if unknown. Default value is "0" for both expressions.
        :param int eof_action: See framesync.
        :param int eval: Set when the expressions for x and y are evaluated. It accepts the following values: init Evaluate expressions once during filter initialization or when a command is processed. frame Evaluate expressions for each incoming frame Default value is frame.
        :param bool shortest: See framesync.
        :param bool repeatlast: See framesync.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#overlay_005fcuda

        """
        filter_node = FilterNode(
            name="overlay_cuda",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _overlay,
            ],
            kwargs={
                "x": x,
                "y": y,
                "eof_action": eof_action,
                "eval": eval,
                "shortest": shortest,
                "repeatlast": repeatlast,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def overlay_opencl(
        self,
        _overlay: "VideoStream",
        *,
        x: int | DefaultInt = DefaultInt(0),
        y: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.9 overlay_opencl
        Overlay one video on top of another.

        It takes two inputs and has one output. The first input is the "main" video on which the second input is overlaid.
        This filter requires same memory layout for all the inputs. So, format conversion may be needed.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int x: Set the x coordinate of the overlaid video on the main video. Default value is 0.
        :param int y: Set the y coordinate of the overlaid video on the main video. Default value is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#overlay_005fopencl

        """
        filter_node = FilterNode(
            name="overlay_opencl",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _overlay,
            ],
            kwargs={
                "x": x,
                "y": y,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def overlay_vaapi(
        self,
        _overlay: "VideoStream",
        *,
        x: str | DefaultStr = DefaultStr("0"),
        y: str | DefaultStr = DefaultStr("0"),
        w: str | DefaultStr = DefaultStr("overlay_iw"),
        h: str | DefaultStr = DefaultStr("overlay_ih*w/overlay_iw"),
        alpha: float | DefaultFloat = DefaultFloat(1.0),
        eof_action: int | Literal["repeat", "endall", "pass"] | DefaultStr = DefaultStr("repeat"),
        shortest: bool | DefaultInt = DefaultInt(0),
        repeatlast: bool | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        13.1 overlay_vaapi
        Overlay one video on the top of another.

        It takes two inputs and has one output. The first input is the "main" video on which the second input is overlaid.

        The filter accepts the following options:


        This filter also supports the framesync options.

        Parameters:
        ----------

        :param str x: Set expressions for the x and y coordinates of the overlaid video on the main video. Default value is "0" for both expressions.
        :param str y: Set expressions for the x and y coordinates of the overlaid video on the main video. Default value is "0" for both expressions.
        :param str w: Set expressions for the width and height the overlaid video on the main video. Default values are ’overlay_iw’ for ’w’ and ’overlay_ih*w/overlay_iw’ for ’h’. The expressions can contain the following parameters: main_w, W main_h, H The main input width and height. overlay_iw overlay_ih The overlay input width and height. overlay_w, w overlay_h, h The overlay output width and height. overlay_x, x overlay_y, y Position of the overlay layer inside of main
        :param str h: Set expressions for the width and height the overlaid video on the main video. Default values are ’overlay_iw’ for ’w’ and ’overlay_ih*w/overlay_iw’ for ’h’. The expressions can contain the following parameters: main_w, W main_h, H The main input width and height. overlay_iw overlay_ih The overlay input width and height. overlay_w, w overlay_h, h The overlay output width and height. overlay_x, x overlay_y, y Position of the overlay layer inside of main
        :param float alpha: Set transparency of overlaid video. Allowed range is 0.0 to 1.0. Higher value means lower transparency. Default value is 1.0.
        :param int eof_action: See framesync.
        :param bool shortest: See framesync.
        :param bool repeatlast: See framesync.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#overlay_005fvaapi

        """
        filter_node = FilterNode(
            name="overlay_vaapi",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _overlay,
            ],
            kwargs={
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "alpha": alpha,
                "eof_action": eof_action,
                "shortest": shortest,
                "repeatlast": repeatlast,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def overlay_vulkan(
        self,
        _overlay: "VideoStream",
        *,
        x: int | DefaultInt = DefaultInt(0),
        y: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        14.11 overlay_vulkan
        Overlay one video on top of another.

        It takes two inputs and has one output. The first input is the "main" video on which the second input is overlaid.
        This filter requires all inputs to use the same pixel format. So, format conversion may be needed.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int x: Set the x coordinate of the overlaid video on the main video. Default value is 0.
        :param int y: Set the y coordinate of the overlaid video on the main video. Default value is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#overlay_005fvulkan

        """
        filter_node = FilterNode(
            name="overlay_vulkan",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _overlay,
            ],
            kwargs={
                "x": x,
                "y": y,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def owdenoise(
        self,
        *,
        depth: int | DefaultInt = DefaultInt(8),
        luma_strength: float | DefaultFloat = DefaultFloat(1.0),
        chroma_strength: float | DefaultFloat = DefaultFloat(1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.185 owdenoise
        Apply Overcomplete Wavelet denoiser.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int depth: Set depth. Larger depth values will denoise lower frequency components more, but slow down filtering. Must be an int in the range 8-16, default is 8.
        :param float luma_strength: Set luma strength. Must be a double value in the range 0-1000, default is 1.0.
        :param float chroma_strength: Set chroma strength. Must be a double value in the range 0-1000, default is 1.0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#owdenoise

        """
        filter_node = FilterNode(
            name="owdenoise",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "depth": depth,
                "luma_strength": luma_strength,
                "chroma_strength": chroma_strength,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def pad(
        self,
        *,
        width: str | DefaultStr = DefaultStr("iw"),
        height: str | DefaultStr = DefaultStr("ih"),
        x: str | DefaultStr = DefaultStr("0"),
        y: str | DefaultStr = DefaultStr("0"),
        color: str | DefaultStr = DefaultStr("black"),
        eval: int | DefaultStr = DefaultStr("EVAL_MODE_INIT"),
        aspect: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.186 pad
        Add paddings to the input image, and place the original input at the
        provided x, y coordinates.

        It accepts the following parameters:


        The value for the width, height, x, and y
        options are expressions containing the following constants:

        Parameters:
        ----------

        :param str width: Specify an expression for the size of the output image with the paddings added. If the value for width or height is 0, the corresponding input size is used for the output. The width expression can reference the value set by the height expression, and vice versa. The default value of width and height is 0.
        :param str height: Specify an expression for the size of the output image with the paddings added. If the value for width or height is 0, the corresponding input size is used for the output. The width expression can reference the value set by the height expression, and vice versa. The default value of width and height is 0.
        :param str x: Specify the offsets to place the input image at within the padded area, with respect to the top/left border of the output image. The x expression can reference the value set by the y expression, and vice versa. The default value of x and y is 0. If x or y evaluate to a negative number, they’ll be changed so the input image is centered on the padded area.
        :param str y: Specify the offsets to place the input image at within the padded area, with respect to the top/left border of the output image. The x expression can reference the value set by the y expression, and vice versa. The default value of x and y is 0. If x or y evaluate to a negative number, they’ll be changed so the input image is centered on the padded area.
        :param str color: Specify the color of the padded area. For the syntax of this option, check the (ffmpeg-utils)"Color" section in the ffmpeg-utils manual. The default value of color is "black".
        :param int eval: Specify when to evaluate width, height, x and y expression. It accepts the following values: ‘init’ Only evaluate expressions once during the filter initialization or when a command is processed. ‘frame’ Evaluate expressions for each incoming frame. Default value is ‘init’.
        :param float aspect: Pad to aspect instead to a resolution.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#pad

        """
        filter_node = FilterNode(
            name="pad",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "width": width,
                "height": height,
                "x": x,
                "y": y,
                "color": color,
                "eval": eval,
                "aspect": aspect,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def pad_opencl(
        self,
        *,
        width: str | DefaultStr = DefaultStr("iw"),
        height: str | DefaultStr = DefaultStr("ih"),
        x: str | DefaultStr = DefaultStr("0"),
        y: str | DefaultStr = DefaultStr("0"),
        color: str | DefaultStr = DefaultStr("black"),
        aspect: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.10 pad_opencl
        Add paddings to the input image, and place the original input at the
        provided x, y coordinates.

        It accepts the following options:


        The value for the width, height, x, and y
        options are expressions containing the following constants:

        Parameters:
        ----------

        :param str width: Specify an expression for the size of the output image with the paddings added. If the value for width or height is 0, the corresponding input size is used for the output. The width expression can reference the value set by the height expression, and vice versa. The default value of width and height is 0.
        :param str height: Specify an expression for the size of the output image with the paddings added. If the value for width or height is 0, the corresponding input size is used for the output. The width expression can reference the value set by the height expression, and vice versa. The default value of width and height is 0.
        :param str x: Specify the offsets to place the input image at within the padded area, with respect to the top/left border of the output image. The x expression can reference the value set by the y expression, and vice versa. The default value of x and y is 0. If x or y evaluate to a negative number, they’ll be changed so the input image is centered on the padded area.
        :param str y: Specify the offsets to place the input image at within the padded area, with respect to the top/left border of the output image. The x expression can reference the value set by the y expression, and vice versa. The default value of x and y is 0. If x or y evaluate to a negative number, they’ll be changed so the input image is centered on the padded area.
        :param str color: Specify the color of the padded area. For the syntax of this option, check the (ffmpeg-utils)"Color" section in the ffmpeg-utils manual.
        :param float aspect: Pad to an aspect instead to a resolution.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#pad_005fopencl

        """
        filter_node = FilterNode(
            name="pad_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "width": width,
                "height": height,
                "x": x,
                "y": y,
                "color": color,
                "aspect": aspect,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def palettegen(
        self,
        *,
        max_colors: int | DefaultInt = DefaultInt(256),
        reserve_transparent: bool | DefaultInt = DefaultInt(1),
        transparency_color: str | DefaultStr = DefaultStr("lime"),
        stats_mode: int | Literal["full", "diff", "single"] | DefaultStr = DefaultStr("full"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.187 palettegen
        Generate one palette for a whole video stream.

        It accepts the following options:


        The filter also exports the frame metadata lavfi.color_quant_ratio
        (nb_color_in / nb_color_out) which you can use to evaluate the degree of
        color quantization of the palette. This information is also visible at
        info logging level.

        Parameters:
        ----------

        :param int max_colors: Set the maximum number of colors to quantize in the palette. Note: the palette will still contain 256 colors; the unused palette entries will be black.
        :param bool reserve_transparent: Create a palette of 255 colors maximum and reserve the last one for transparency. Reserving the transparency color is useful for GIF optimization. If not set, the maximum of colors in the palette will be 256. You probably want to disable this option for a standalone image. Set by default.
        :param str transparency_color: Set the color that will be used as background for transparency.
        :param int stats_mode: Set statistics mode. It accepts the following values: ‘full’ Compute full frame histograms. ‘diff’ Compute histograms only for the part that differs from previous frame. This might be relevant to give more importance to the moving part of your input if the background is static. ‘single’ Compute new histogram for each frame. Default value is full.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#palettegen

        """
        filter_node = FilterNode(
            name="palettegen",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "max_colors": max_colors,
                "reserve_transparent": reserve_transparent,
                "transparency_color": transparency_color,
                "stats_mode": stats_mode,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def paletteuse(
        self,
        _palette: "VideoStream",
        *,
        dither: int
        | Literal["bayer", "heckbert", "floyd_steinberg", "sierra2", "sierra2_4a", "sierra3", "burkes", "atkinson"]
        | DefaultStr = DefaultStr("sierra2_4a"),
        bayer_scale: int | DefaultInt = DefaultInt(2),
        diff_mode: int | Literal["rectangle"] | DefaultStr = DefaultStr("DIFF_MODE_NONE"),
        new: bool | DefaultInt = DefaultInt(0),
        alpha_threshold: int | DefaultInt = DefaultInt(128),
        debug_kdtree: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.188 paletteuse
        Use a palette to downsample an input video stream.

        The filter takes two inputs: one video stream and a palette. The palette must
        be a 256 pixels image.

        It accepts the following options:

        Parameters:
        ----------

        :param int dither: Select dithering mode. Available algorithms are: ‘bayer’ Ordered 8x8 bayer dithering (deterministic) ‘heckbert’ Dithering as defined by Paul Heckbert in 1982 (simple error diffusion). Note: this dithering is sometimes considered "wrong" and is included as a reference. ‘floyd_steinberg’ Floyd and Steingberg dithering (error diffusion) ‘sierra2’ Frankie Sierra dithering v2 (error diffusion) ‘sierra2_4a’ Frankie Sierra dithering v2 "Lite" (error diffusion) ‘sierra3’ Frankie Sierra dithering v3 (error diffusion) ‘burkes’ Burkes dithering (error diffusion) ‘atkinson’ Atkinson dithering by Bill Atkinson at Apple Computer (error diffusion) ‘none’ Disable dithering. Default is sierra2_4a.
        :param int bayer_scale: When bayer dithering is selected, this option defines the scale of the pattern (how much the crosshatch pattern is visible). A low value means more visible pattern for less banding, and higher value means less visible pattern at the cost of more banding. The option must be an integer value in the range [0,5]. Default is 2.
        :param int diff_mode: If set, define the zone to process ‘rectangle’ Only the changing rectangle will be reprocessed. This is similar to GIF cropping/offsetting compression mechanism. This option can be useful for speed if only a part of the image is changing, and has use cases such as limiting the scope of the error diffusal dither to the rectangle that bounds the moving scene (it leads to more deterministic output if the scene doesn’t change much, and as a result less moving noise and better GIF compression). Default is none.
        :param bool new: Take new palette for each output frame.
        :param int alpha_threshold: Sets the alpha threshold for transparency. Alpha values above this threshold will be treated as completely opaque, and values below this threshold will be treated as completely transparent. The option must be an integer value in the range [0,255]. Default is 128.
        :param str debug_kdtree: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#paletteuse

        """
        filter_node = FilterNode(
            name="paletteuse",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _palette,
            ],
            kwargs={
                "dither": dither,
                "bayer_scale": bayer_scale,
                "diff_mode": diff_mode,
                "new": new,
                "alpha_threshold": alpha_threshold,
                "debug_kdtree": debug_kdtree,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def perms(
        self,
        *,
        mode: int | Literal["none", "ro", "rw", "toggle", "random"] | DefaultStr = DefaultStr("none"),
        seed: int | DefaultInt = DefaultInt(-1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        18.14 perms, aperms
        Set read/write permissions for the output frames.

        These filters are mainly aimed at developers to test direct path in the
        following filter in the filtergraph.

        The filters accept the following options:


        Note: in case of auto-inserted filter between the permission filter and the
        following one, the permission might not be received as expected in that
        following filter. Inserting a format or aformat filter before the
        perms/aperms filter can avoid this problem.

        Parameters:
        ----------

        :param int mode: Select the permissions mode. It accepts the following values: ‘none’ Do nothing. This is the default. ‘ro’ Set all the output frames read-only. ‘rw’ Set all the output frames directly writable. ‘toggle’ Make the frame read-only if writable, and writable if read-only. ‘random’ Set each output frame read-only or writable randomly.
        :param int seed: Set the seed for the random mode, must be an integer included between 0 and UINT32_MAX. If not specified, or if explicitly set to -1, the filter will try to use a good random seed on a best effort basis.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#perms_002c-aperms

        """
        filter_node = FilterNode(
            name="perms",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "seed": seed,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def perspective(
        self,
        *,
        x0: str | DefaultStr = DefaultStr("0"),
        y0: str | DefaultStr = DefaultStr("0"),
        x1: str | DefaultStr = DefaultStr("W"),
        y1: str | DefaultStr = DefaultStr("0"),
        x2: str | DefaultStr = DefaultStr("0"),
        y2: str | DefaultStr = DefaultStr("H"),
        x3: str | DefaultStr = DefaultStr("W"),
        y3: str | DefaultStr = DefaultStr("H"),
        interpolation: int | Literal["linear", "cubic"] | DefaultStr = DefaultStr("linear"),
        sense: int | Literal["source", "destination"] | DefaultStr = DefaultStr("source"),
        eval: int | DefaultStr = DefaultStr("EVAL_MODE_INIT"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.189 perspective
        Correct perspective of video not recorded perpendicular to the screen.

        A description of the accepted parameters follows.

        Parameters:
        ----------

        :param str x0: None
        :param str y0: None
        :param str x1: None
        :param str y1: None
        :param str x2: None
        :param str y2: None
        :param str x3: None
        :param str y3: None
        :param int interpolation: None
        :param int sense: None
        :param int eval: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#perspective

        """
        filter_node = FilterNode(
            name="perspective",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "x0": x0,
                "y0": y0,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "x3": x3,
                "y3": y3,
                "interpolation": interpolation,
                "sense": sense,
                "eval": eval,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def phase(
        self,
        *,
        mode: int | Literal["p", "t", "b", "T", "B", "u", "U", "a", "A"] | DefaultStr = DefaultStr("A"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.190 phase
        Delay interlaced video by one field time so that the field order changes.

        The intended use is to fix PAL movies that have been captured with the
        opposite field order to the film-to-video transfer.

        A description of the accepted parameters follows.

        Parameters:
        ----------

        :param int mode: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#phase

        """
        filter_node = FilterNode(
            name="phase",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def photosensitivity(
        self,
        *,
        frames: int | DefaultInt = DefaultInt(30),
        threshold: float | DefaultFloat = DefaultFloat(1.0),
        skip: int | DefaultInt = DefaultInt(1),
        bypass: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.191 photosensitivity
        Reduce various flashes in video, so to help users with epilepsy.

        It accepts the following options:

        Parameters:
        ----------

        :param int frames: Set how many frames to use when filtering. Default is 30.
        :param float threshold: Set detection threshold factor. Default is 1. Lower is stricter.
        :param int skip: Set how many pixels to skip when sampling frames. Default is 1. Allowed range is from 1 to 1024.
        :param bool bypass: Leave frames unchanged. Default is disabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#photosensitivity

        """
        filter_node = FilterNode(
            name="photosensitivity",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "frames": frames,
                "threshold": threshold,
                "skip": skip,
                "bypass": bypass,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def pixdesctest(self, **kwargs: Any) -> "VideoStream":
        """

        11.192 pixdesctest
        Pixel format descriptor test filter, mainly useful for internal
        testing. The output video should be equal to the input video.

        For example:

        format=monow, pixdesctest

        can be used to test the monowhite pixel format descriptor definition.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#pixdesctest

        """
        filter_node = FilterNode(
            name="pixdesctest",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def pixelize(
        self,
        *,
        width: int | DefaultInt = DefaultInt(16),
        height: int | DefaultInt = DefaultInt(16),
        mode: int | Literal["avg", "min", "max"] | DefaultStr = DefaultStr(0),
        planes: str | DefaultStr = DefaultStr(15),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.193 pixelize
        Apply pixelization to video stream.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int width: Set block dimensions that will be used for pixelization. Default value is 16.
        :param int height: Set block dimensions that will be used for pixelization. Default value is 16.
        :param int mode: Set the mode of pixelization used. Possible values are: ‘avg’ ‘min’ ‘max’ Default value is avg.
        :param str planes: Set what planes to filter. Default is to filter all planes.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#pixelize

        """
        filter_node = FilterNode(
            name="pixelize",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "width": width,
                "height": height,
                "mode": mode,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def pixscope(
        self,
        *,
        x: float | DefaultFloat = DefaultFloat(0.5),
        y: float | DefaultFloat = DefaultFloat(0.5),
        w: int | DefaultInt = DefaultInt(7),
        h: int | DefaultInt = DefaultInt(7),
        o: float | DefaultFloat = DefaultFloat(0.5),
        wx: float | DefaultFloat = DefaultFloat(-1.0),
        wy: float | DefaultFloat = DefaultFloat(-1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.194 pixscope
        Display sample values of color channels. Mainly useful for checking color
        and levels. Minimum supported resolution is 640x480.

        The filters accept the following options:

        Parameters:
        ----------

        :param float x: Set scope X position, relative offset on X axis.
        :param float y: Set scope Y position, relative offset on Y axis.
        :param int w: Set scope width.
        :param int h: Set scope height.
        :param float o: Set window opacity. This window also holds statistics about pixel area.
        :param float wx: Set window X position, relative offset on X axis.
        :param float wy: Set window Y position, relative offset on Y axis.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#pixscope

        """
        filter_node = FilterNode(
            name="pixscope",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "o": o,
                "wx": wx,
                "wy": wy,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def pp(self, *, subfilters: str | DefaultStr = DefaultStr("de"), **kwargs: Any) -> "VideoStream":
        """

        11.195 pp
        Enable the specified chain of postprocessing subfilters using libpostproc. This
        library should be automatically selected with a GPL build (--enable-gpl).
        Subfilters must be separated by ’/’ and can be disabled by prepending a ’-’.
        Each subfilter and some options have a short and a long name that can be used
        interchangeably, i.e. dr/dering are the same.

        The filters accept the following options:


        All subfilters share common options to determine their scope:


        These options can be appended after the subfilter name, separated by a ’|’.

        Available subfilters are:


        The horizontal and vertical deblocking filters share the difference and
        flatness values so you cannot set different horizontal and vertical
        thresholds.

        Parameters:
        ----------

        :param str subfilters: Set postprocessing subfilters string.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#pp

        """
        filter_node = FilterNode(
            name="pp",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "subfilters": subfilters,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def pp7(
        self,
        *,
        qp: int | DefaultInt = DefaultInt(0),
        mode: int | Literal["hard", "soft", "medium"] | DefaultStr = DefaultStr("medium"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.196 pp7
        Apply Postprocessing filter 7. It is variant of the spp filter,
        similar to spp = 6 with 7 point DCT, where only the center sample is
        used after IDCT.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int qp: Force a constant quantization parameter. It accepts an integer in range 0 to 63. If not set, the filter will use the QP from the video stream (if available).
        :param int mode: Set thresholding mode. Available modes are: ‘hard’ Set hard thresholding. ‘soft’ Set soft thresholding (better de-ringing effect, but likely blurrier). ‘medium’ Set medium thresholding (good results, default).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#pp7

        """
        filter_node = FilterNode(
            name="pp7",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "qp": qp,
                "mode": mode,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def prewitt(
        self,
        *,
        planes: int | DefaultInt = DefaultInt(15),
        scale: float | DefaultFloat = DefaultFloat(1.0),
        delta: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.198 prewitt
        Apply prewitt operator to input video stream.

        The filter accepts the following option:

        Parameters:
        ----------

        :param int planes: Set which planes will be processed, unprocessed planes will be copied. By default value 0xf, all planes will be processed.
        :param float scale: Set value which will be multiplied with filtered result.
        :param float delta: Set value which will be added to filtered result.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#prewitt

        """
        filter_node = FilterNode(
            name="prewitt",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "planes": planes,
                "scale": scale,
                "delta": delta,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def prewitt_opencl(
        self,
        *,
        planes: int | DefaultInt = DefaultInt(15),
        scale: float | DefaultFloat = DefaultFloat(1.0),
        delta: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.11 prewitt_opencl
        Apply the Prewitt operator (https://en.wikipedia.org/wiki/Prewitt_operator) to input video stream.

        The filter accepts the following option:

        Parameters:
        ----------

        :param int planes: Set which planes to filter. Default value is 0xf, by which all planes are processed.
        :param float scale: Set value which will be multiplied with filtered result. Range is [0.0, 65535] and default value is 1.0.
        :param float delta: Set value which will be added to filtered result. Range is [-65535, 65535] and default value is 0.0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#prewitt_005fopencl

        """
        filter_node = FilterNode(
            name="prewitt_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "planes": planes,
                "scale": scale,
                "delta": delta,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def pseudocolor(
        self,
        *,
        c0: str | DefaultStr = DefaultStr("val"),
        c1: str | DefaultStr = DefaultStr("val"),
        c2: str | DefaultStr = DefaultStr("val"),
        c3: str | DefaultStr = DefaultStr("val"),
        index: int | DefaultInt = DefaultInt(0),
        preset: int
        | Literal[
            "none",
            "magma",
            "inferno",
            "plasma",
            "viridis",
            "turbo",
            "cividis",
            "range1",
            "range2",
            "shadows",
            "highlights",
            "solar",
            "nominal",
            "preferred",
            "total",
            "spectral",
            "cool",
            "heat",
            "fiery",
            "blues",
            "green",
            "helix",
        ]
        | DefaultStr = DefaultStr("none"),
        opacity: float | DefaultFloat = DefaultFloat(1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.199 pseudocolor
        Alter frame colors in video with pseudocolors.

        This filter accepts the following options:


        Each of the expression options specifies the expression to use for computing
        the lookup table for the corresponding pixel component values.

        The expressions can contain the following constants and functions:


        All expressions default to "val".

        Parameters:
        ----------

        :param str c0: set pixel first component expression
        :param str c1: set pixel second component expression
        :param str c2: set pixel third component expression
        :param str c3: set pixel fourth component expression, corresponds to the alpha component
        :param int index: set component to use as base for altering colors
        :param int preset: Pick one of built-in LUTs. By default is set to none. Available LUTs: ‘magma’ ‘inferno’ ‘plasma’ ‘viridis’ ‘turbo’ ‘cividis’ ‘range1’ ‘range2’ ‘shadows’ ‘highlights’ ‘solar’ ‘nominal’ ‘preferred’ ‘total’ ‘spectral’ ‘cool’ ‘heat’ ‘fiery’ ‘blues’ ‘green’ ‘helix’
        :param float opacity: Set opacity of output colors. Allowed range is from 0 to 1. Default value is set to 1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#pseudocolor

        """
        filter_node = FilterNode(
            name="pseudocolor",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "c0": c0,
                "c1": c1,
                "c2": c2,
                "c3": c3,
                "index": index,
                "preset": preset,
                "opacity": opacity,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def psnr(
        self,
        _reference: "VideoStream",
        *,
        stats_file: str,
        stats_version: int | DefaultInt = DefaultInt(1),
        output_max: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.200 psnr
        Obtain the average, maximum and minimum PSNR (Peak Signal to Noise
        Ratio) between two input videos.

        This filter takes in input two input videos, the first input is
        considered the "main" source and is passed unchanged to the
        output. The second input is used as a "reference" video for computing
        the PSNR.

        Both video inputs must have the same resolution and pixel format for
        this filter to work correctly. Also it assumes that both inputs
        have the same number of frames, which are compared one by one.

        The obtained average PSNR is printed through the logging system.

        The filter stores the accumulated MSE (mean squared error) of each
        frame, and at the end of the processing it is averaged across all frames
        equally, and the following formula is applied to obtain the PSNR:


        PSNR = 10*log10(MAX^2/MSE)

        Where MAX is the average of the maximum values of each component of the
        image.

        The description of the accepted parameters follows.


        This filter also supports the framesync options.

        The file printed if stats_file is selected, contains a sequence of
        key/value pairs of the form key:value for each compared
        couple of frames.

        If a stats_version greater than 1 is specified, a header line precedes
        the list of per-frame-pair stats, with key value pairs following the frame
        format with the following parameters:


        A description of each shown per-frame-pair parameter follows:

        Parameters:
        ----------

        :param str stats_file: If specified the filter will use the named file to save the PSNR of each individual frame. When filename equals "-" the data is sent to standard output.
        :param int stats_version: Specifies which version of the stats file format to use. Details of each format are written below. Default value is 1.
        :param bool output_max: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#psnr

        """
        filter_node = FilterNode(
            name="psnr",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _reference,
            ],
            kwargs={
                "stats_file": stats_file,
                "stats_version": stats_version,
                "output_max": output_max,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def pullup(
        self,
        *,
        jl: int | DefaultInt = DefaultInt(1),
        jr: int | DefaultInt = DefaultInt(1),
        jt: int | DefaultInt = DefaultInt(4),
        jb: int | DefaultInt = DefaultInt(4),
        sb: bool | DefaultInt = DefaultInt(0),
        mp: int | Literal["y", "u", "v"] | DefaultStr = DefaultStr("y"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.201 pullup
        Pulldown reversal (inverse telecine) filter, capable of handling mixed
        hard-telecine, 24000/1001 fps progressive, and 30000/1001 fps progressive
        content.

        The pullup filter is designed to take advantage of future context in making
        its decisions. This filter is stateless in the sense that it does not lock
        onto a pattern to follow, but it instead looks forward to the following
        fields in order to identify matches and rebuild progressive frames.

        To produce content with an even framerate, insert the fps filter after
        pullup, use fps=24000/1001 if the input frame rate is 29.97fps,
        fps=24 for 30fps and the (rare) telecined 25fps input.

        The filter accepts the following options:


        For best results (without duplicated frames in the output file) it is
        necessary to change the output frame rate. For example, to inverse
        telecine NTSC input:

        ffmpeg -i input -vf pullup -r 24000/1001 ...

        Parameters:
        ----------

        :param int jl: These options set the amount of "junk" to ignore at the left, right, top, and bottom of the image, respectively. Left and right are in units of 8 pixels, while top and bottom are in units of 2 lines. The default is 8 pixels on each side.
        :param int jr: These options set the amount of "junk" to ignore at the left, right, top, and bottom of the image, respectively. Left and right are in units of 8 pixels, while top and bottom are in units of 2 lines. The default is 8 pixels on each side.
        :param int jt: These options set the amount of "junk" to ignore at the left, right, top, and bottom of the image, respectively. Left and right are in units of 8 pixels, while top and bottom are in units of 2 lines. The default is 8 pixels on each side.
        :param int jb: These options set the amount of "junk" to ignore at the left, right, top, and bottom of the image, respectively. Left and right are in units of 8 pixels, while top and bottom are in units of 2 lines. The default is 8 pixels on each side.
        :param bool sb: Set the strict breaks. Setting this option to 1 will reduce the chances of filter generating an occasional mismatched frame, but it may also cause an excessive number of frames to be dropped during high motion sequences. Conversely, setting it to -1 will make filter match fields more easily. This may help processing of video where there is slight blurring between the fields, but may also cause there to be interlaced frames in the output. Default value is 0.
        :param int mp: Set the metric plane to use. It accepts the following values: ‘l’ Use luma plane. ‘u’ Use chroma blue plane. ‘v’ Use chroma red plane. This option may be set to use chroma plane instead of the default luma plane for doing filter’s computations. This may improve accuracy on very clean source material, but more likely will decrease accuracy, especially if there is chroma noise (rainbow effect) or any grayscale video. The main purpose of setting mp to a chroma plane is to reduce CPU load and make pullup usable in realtime on slow machines.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#pullup

        """
        filter_node = FilterNode(
            name="pullup",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "jl": jl,
                "jr": jr,
                "jt": jt,
                "jb": jb,
                "sb": sb,
                "mp": mp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def qp(self, *, qp: str, **kwargs: Any) -> "VideoStream":
        """

        11.202 qp
        Change video quantization parameters (QP).

        The filter accepts the following option:


        The expression is evaluated through the eval API and can contain, among others,
        the following constants:

        Parameters:
        ----------

        :param str qp: Set expression for quantization parameter.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#qp

        """
        filter_node = FilterNode(
            name="qp",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "qp": qp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def random(
        self, *, frames: int | DefaultInt = DefaultInt(30), seed: int | DefaultInt = DefaultInt(-1), **kwargs: Any
    ) -> "VideoStream":
        """

        11.203 random
        Flush video frames from internal cache of frames into a random order.
        No frame is discarded.
        Inspired by frei0r nervous filter.

        Parameters:
        ----------

        :param int frames: Set size in number of frames of internal cache, in range from 2 to 512. Default is 30.
        :param int seed: Set seed for random number generator, must be an integer included between 0 and UINT32_MAX. If not specified, or if explicitly set to less than 0, the filter will try to use a good random seed on a best effort basis.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#random

        """
        filter_node = FilterNode(
            name="random",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "frames": frames,
                "seed": seed,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def readeia608(
        self,
        *,
        scan_min: int | DefaultInt = DefaultInt(0),
        scan_max: int | DefaultInt = DefaultInt(29),
        spw: float | DefaultFloat = DefaultFloat(0.27),
        chp: bool | DefaultInt = DefaultInt(0),
        lp: bool | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.204 readeia608
        Read closed captioning (EIA-608) information from the top lines of a video frame.

        This filter adds frame metadata for lavfi.readeia608.X.cc and
        lavfi.readeia608.X.line, where X is the number of the identified line
        with EIA-608 data (starting from 0). A description of each metadata value follows:


        This filter accepts the following options:

        Parameters:
        ----------

        :param int scan_min: Set the line to start scanning for EIA-608 data. Default is 0.
        :param int scan_max: Set the line to end scanning for EIA-608 data. Default is 29.
        :param float spw: Set the ratio of width reserved for sync code detection. Default is 0.27. Allowed range is [0.1 - 0.7].
        :param bool chp: Enable checking the parity bit. In the event of a parity error, the filter will output 0x00 for that character. Default is false.
        :param bool lp: Lowpass lines prior to further processing. Default is enabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#readeia608

        """
        filter_node = FilterNode(
            name="readeia608",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "scan_min": scan_min,
                "scan_max": scan_max,
                "spw": spw,
                "chp": chp,
                "lp": lp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def readvitc(
        self,
        *,
        scan_max: int | DefaultInt = DefaultInt(45),
        thr_b: float | DefaultFloat = DefaultFloat(0.2),
        thr_w: float | DefaultFloat = DefaultFloat(0.6),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.205 readvitc
        Read vertical interval timecode (VITC) information from the top lines of a
        video frame.

        The filter adds frame metadata key lavfi.readvitc.tc_str with the
        timecode value, if a valid timecode has been detected. Further metadata key
        lavfi.readvitc.found is set to 0/1 depending on whether
        timecode data has been found or not.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int scan_max: Set the maximum number of lines to scan for VITC data. If the value is set to -1 the full video frame is scanned. Default is 45.
        :param float thr_b: Set the luma threshold for black. Accepts float numbers in the range [0.0,1.0], default value is 0.2. The value must be equal or less than thr_w.
        :param float thr_w: Set the luma threshold for white. Accepts float numbers in the range [0.0,1.0], default value is 0.6. The value must be equal or greater than thr_b.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#readvitc

        """
        filter_node = FilterNode(
            name="readvitc",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "scan_max": scan_max,
                "thr_b": thr_b,
                "thr_w": thr_w,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def realtime(
        self,
        *,
        limit: int | DefaultInt = DefaultInt(2000000),
        speed: float | DefaultFloat = DefaultFloat(1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        18.15 realtime, arealtime
        Slow down filtering to match real time approximately.

        These filters will pause the filtering for a variable amount of time to
        match the output rate with the input timestamps.
        They are similar to the re option to ffmpeg.

        They accept the following options:

        Parameters:
        ----------

        :param int limit: Time limit for the pauses. Any pause longer than that will be considered a timestamp discontinuity and reset the timer. Default is 2 seconds.
        :param float speed: Speed factor for processing. The value must be a float larger than zero. Values larger than 1.0 will result in faster than realtime processing, smaller will slow processing down. The limit is automatically adapted accordingly. Default is 1.0. A processing speed faster than what is possible without these filters cannot be achieved.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#realtime_002c-arealtime

        """
        filter_node = FilterNode(
            name="realtime",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "limit": limit,
                "speed": speed,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def remap(
        self,
        _xmap: "VideoStream",
        _ymap: "VideoStream",
        *,
        format: int | DefaultInt = DefaultInt(0),
        fill: str | DefaultStr = DefaultStr("black"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.206 remap
        Remap pixels using 2nd: Xmap and 3rd: Ymap input video stream.

        Destination pixel at position (X, Y) will be picked from source (x, y) position
        where x = Xmap(X, Y) and y = Ymap(X, Y). If mapping values are out of range, zero
        value for pixel will be used for destination pixel.

        Xmap and Ymap input video streams must be of same dimensions. Output video stream
        will have Xmap/Ymap video stream dimensions.
        Xmap and Ymap input video streams are 16bit depth, single channel.

        Parameters:
        ----------

        :param int format: Specify pixel format of output from this filter. Can be color or gray. Default is color.
        :param str fill: Specify the color of the unmapped pixels. For the syntax of this option, check the (ffmpeg-utils)"Color" section in the ffmpeg-utils manual. Default color is black.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#remap

        """
        filter_node = FilterNode(
            name="remap",
            input_typings=[StreamType.video, StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _xmap,
                _ymap,
            ],
            kwargs={
                "format": format,
                "fill": fill,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def remap_opencl(
        self,
        _xmap: "VideoStream",
        _ymap: "VideoStream",
        *,
        interp: int | Literal["near", "linear"] | DefaultStr = DefaultStr("linear"),
        fill: str | DefaultStr = DefaultStr("black"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.13 remap_opencl
        Remap pixels using 2nd: Xmap and 3rd: Ymap input video stream.

        Destination pixel at position (X, Y) will be picked from source (x, y) position
        where x = Xmap(X, Y) and y = Ymap(X, Y). If mapping values are out of range, zero
        value for pixel will be used for destination pixel.

        Xmap and Ymap input video streams must be of same dimensions. Output video stream
        will have Xmap/Ymap video stream dimensions.
        Xmap and Ymap input video streams are 32bit float pixel format, single channel.

        Parameters:
        ----------

        :param int interp: Specify interpolation used for remapping of pixels. Allowed values are near and linear. Default value is linear.
        :param str fill: Specify the color of the unmapped pixels. For the syntax of this option, check the (ffmpeg-utils)"Color" section in the ffmpeg-utils manual. Default color is black.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#remap_005fopencl

        """
        filter_node = FilterNode(
            name="remap_opencl",
            input_typings=[StreamType.video, StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _xmap,
                _ymap,
            ],
            kwargs={
                "interp": interp,
                "fill": fill,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def removegrain(
        self,
        *,
        m0: int | DefaultInt = DefaultInt(0),
        m1: int | DefaultInt = DefaultInt(0),
        m2: int | DefaultInt = DefaultInt(0),
        m3: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.207 removegrain
        The removegrain filter is a spatial denoiser for progressive video.


        Range of mode is from 0 to 24. Description of each mode follows:

        Parameters:
        ----------

        :param int m0: Set mode for the first plane.
        :param int m1: Set mode for the second plane.
        :param int m2: Set mode for the third plane.
        :param int m3: Set mode for the fourth plane.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#removegrain

        """
        filter_node = FilterNode(
            name="removegrain",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "m0": m0,
                "m1": m1,
                "m2": m2,
                "m3": m3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def removelogo(self, *, filename: str, **kwargs: Any) -> "VideoStream":
        """

        11.208 removelogo
        Suppress a TV station logo, using an image file to determine which
        pixels comprise the logo. It works by filling in the pixels that
        comprise the logo with neighboring pixels.

        The filter accepts the following options:


        Pixels in the provided bitmap image with a value of zero are not
        considered part of the logo, non-zero pixels are considered part of
        the logo. If you use white (255) for the logo and black (0) for the
        rest, you will be safe. For making the filter bitmap, it is
        recommended to take a screen capture of a black frame with the logo
        visible, and then using a threshold filter followed by the erode
        filter once or twice.

        If needed, little splotches can be fixed manually. Remember that if
        logo pixels are not covered, the filter quality will be much
        reduced. Marking too many pixels as part of the logo does not hurt as
        much, but it will increase the amount of blurring needed to cover over
        the image and will destroy more information than necessary, and extra
        pixels will slow things down on a large logo.

        Parameters:
        ----------

        :param str filename: Set the filter bitmap file, which can be any image format supported by libavformat. The width and height of the image file must match those of the video stream being processed.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#removelogo

        """
        filter_node = FilterNode(
            name="removelogo",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "filename": filename,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def repeatfields(self, **kwargs: Any) -> "VideoStream":
        """

        11.209 repeatfields
        This filter uses the repeat_field flag from the Video ES headers and hard repeats
        fields based on its value.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#repeatfields

        """
        filter_node = FilterNode(
            name="repeatfields",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def reverse(self, **kwargs: Any) -> "VideoStream":
        """

        11.210 reverse
        Reverse a video clip.

        Warning: This filter requires memory to buffer the entire clip, so trimming
        is suggested.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#reverse

        """
        filter_node = FilterNode(
            name="reverse",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def rgbashift(
        self,
        *,
        rh: int | DefaultInt = DefaultInt(0),
        rv: int | DefaultInt = DefaultInt(0),
        gh: int | DefaultInt = DefaultInt(0),
        gv: int | DefaultInt = DefaultInt(0),
        bh: int | DefaultInt = DefaultInt(0),
        bv: int | DefaultInt = DefaultInt(0),
        ah: int | DefaultInt = DefaultInt(0),
        av: int | DefaultInt = DefaultInt(0),
        edge: int | Literal["smear", "wrap"] | DefaultStr = DefaultStr("smear"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.211 rgbashift
        Shift R/G/B/A pixels horizontally and/or vertically.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int rh: Set amount to shift red horizontally.
        :param int rv: Set amount to shift red vertically.
        :param int gh: Set amount to shift green horizontally.
        :param int gv: Set amount to shift green vertically.
        :param int bh: Set amount to shift blue horizontally.
        :param int bv: Set amount to shift blue vertically.
        :param int ah: Set amount to shift alpha horizontally.
        :param int av: Set amount to shift alpha vertically.
        :param int edge: Set edge mode, can be smear, default, or warp.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#rgbashift

        """
        filter_node = FilterNode(
            name="rgbashift",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "rh": rh,
                "rv": rv,
                "gh": gh,
                "gv": gv,
                "bh": bh,
                "bv": bv,
                "ah": ah,
                "av": av,
                "edge": edge,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def roberts(
        self,
        *,
        planes: int | DefaultInt = DefaultInt(15),
        scale: float | DefaultFloat = DefaultFloat(1.0),
        delta: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.212 roberts
        Apply roberts cross operator to input video stream.

        The filter accepts the following option:

        Parameters:
        ----------

        :param int planes: Set which planes will be processed, unprocessed planes will be copied. By default value 0xf, all planes will be processed.
        :param float scale: Set value which will be multiplied with filtered result.
        :param float delta: Set value which will be added to filtered result.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#roberts

        """
        filter_node = FilterNode(
            name="roberts",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "planes": planes,
                "scale": scale,
                "delta": delta,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def roberts_opencl(
        self,
        *,
        planes: int | DefaultInt = DefaultInt(15),
        scale: float | DefaultFloat = DefaultFloat(1.0),
        delta: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.14 roberts_opencl
        Apply the Roberts cross operator (https://en.wikipedia.org/wiki/Roberts_cross) to input video stream.

        The filter accepts the following option:

        Parameters:
        ----------

        :param int planes: Set which planes to filter. Default value is 0xf, by which all planes are processed.
        :param float scale: Set value which will be multiplied with filtered result. Range is [0.0, 65535] and default value is 1.0.
        :param float delta: Set value which will be added to filtered result. Range is [-65535, 65535] and default value is 0.0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#roberts_005fopencl

        """
        filter_node = FilterNode(
            name="roberts_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "planes": planes,
                "scale": scale,
                "delta": delta,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def rotate(
        self,
        *,
        angle: str | DefaultStr = DefaultStr("0"),
        out_w: str | DefaultStr = DefaultStr("iw"),
        out_h: str | DefaultStr = DefaultStr("ih"),
        fillcolor: str | DefaultStr = DefaultStr("black"),
        bilinear: bool | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.213 rotate
        Rotate video by an arbitrary angle expressed in radians.

        The filter accepts the following options:

        A description of the optional parameters follows.

        The expressions for the angle and the output size can contain the
        following constants and functions:

        Parameters:
        ----------

        :param str angle: Set an expression for the angle by which to rotate the input video clockwise, expressed as a number of radians. A negative value will result in a counter-clockwise rotation. By default it is set to "0". This expression is evaluated for each frame.
        :param str out_w: Set the output width expression, default value is "iw". This expression is evaluated just once during configuration.
        :param str out_h: Set the output height expression, default value is "ih". This expression is evaluated just once during configuration.
        :param str fillcolor: Set the color used to fill the output area not covered by the rotated image. For the general syntax of this option, check the (ffmpeg-utils)"Color" section in the ffmpeg-utils manual. If the special value "none" is selected then no background is printed (useful for example if the background is never shown). Default value is "black".
        :param bool bilinear: Enable bilinear interpolation if set to 1, a value of 0 disables it. Default value is 1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#rotate

        """
        filter_node = FilterNode(
            name="rotate",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "angle": angle,
                "out_w": out_w,
                "out_h": out_h,
                "fillcolor": fillcolor,
                "bilinear": bilinear,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def sab(
        self,
        *,
        luma_radius: float | DefaultFloat = DefaultFloat(1.0),
        luma_pre_filter_radius: float | DefaultFloat = DefaultFloat(1.0),
        luma_strength: float | DefaultFloat = DefaultFloat(1.0),
        chroma_radius: float | DefaultStr = DefaultStr("0.1 -1"),
        chroma_pre_filter_radius: float | DefaultStr = DefaultStr("0.1 -1"),
        chroma_strength: float | DefaultStr = DefaultStr("0.1 -1"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.214 sab
        Apply Shape Adaptive Blur.

        The filter accepts the following options:


        Each chroma option value, if not explicitly specified, is set to the
        corresponding luma option value.

        Parameters:
        ----------

        :param float luma_radius: Set luma blur filter strength, must be a value in range 0.1-4.0, default value is 1.0. A greater value will result in a more blurred image, and in slower processing.
        :param float luma_pre_filter_radius: Set luma pre-filter radius, must be a value in the 0.1-2.0 range, default value is 1.0.
        :param float luma_strength: Set luma maximum difference between pixels to still be considered, must be a value in the 0.1-100.0 range, default value is 1.0.
        :param float chroma_radius: Set chroma blur filter strength, must be a value in range -0.9-4.0. A greater value will result in a more blurred image, and in slower processing.
        :param float chroma_pre_filter_radius: Set chroma pre-filter radius, must be a value in the -0.9-2.0 range.
        :param float chroma_strength: Set chroma maximum difference between pixels to still be considered, must be a value in the -0.9-100.0 range.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#sab

        """
        filter_node = FilterNode(
            name="sab",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "luma_radius": luma_radius,
                "luma_pre_filter_radius": luma_pre_filter_radius,
                "luma_strength": luma_strength,
                "chroma_radius": chroma_radius,
                "chroma_pre_filter_radius": chroma_pre_filter_radius,
                "chroma_strength": chroma_strength,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def scale(
        self,
        *,
        w: str,
        h: str,
        flags: str | DefaultStr = DefaultStr(""),
        interl: bool | DefaultInt = DefaultInt(0),
        size: str,
        in_color_matrix: int
        | Literal["auto", "bt601", "bt470", "smpte170m", "bt709", "fcc", "smpte240m", "bt2020"]
        | DefaultStr = DefaultStr("auto"),
        out_color_matrix: int
        | Literal["auto", "bt601", "bt470", "smpte170m", "bt709", "fcc", "smpte240m", "bt2020"]
        | DefaultStr = DefaultStr("AVCOL_SPC_UNSPECIFIED"),
        in_range: int
        | Literal["auto", "unknown", "full", "limited", "jpeg", "mpeg", "tv", "pc"]
        | DefaultStr = DefaultStr("auto"),
        out_range: int
        | Literal["auto", "unknown", "full", "limited", "jpeg", "mpeg", "tv", "pc"]
        | DefaultStr = DefaultStr("auto"),
        in_v_chr_pos: int | DefaultInt = DefaultInt(-513),
        in_h_chr_pos: int | DefaultInt = DefaultInt(-513),
        out_v_chr_pos: int | DefaultInt = DefaultInt(-513),
        out_h_chr_pos: int | DefaultInt = DefaultInt(-513),
        force_original_aspect_ratio: int
        | Literal["disable", "decrease", "increase"]
        | DefaultStr = DefaultStr("disable"),
        force_divisible_by: int | DefaultInt = DefaultInt(1),
        param0: float | DefaultFloat = DefaultFloat(1.7976931348623157e308),
        param1: float | DefaultFloat = DefaultFloat(1.7976931348623157e308),
        eval: int | DefaultStr = DefaultStr("EVAL_MODE_INIT"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.215 scale
        Scale (resize) the input video, using the libswscale library.

        The scale filter forces the output display aspect ratio to be the same
        of the input, by changing the output sample aspect ratio.

        If the input image format is different from the format requested by
        the next filter, the scale filter will convert the input to the
        requested format.

        Parameters:
        ----------

        :param str w: None
        :param str h: None
        :param str flags: None
        :param bool interl: None
        :param str size: None
        :param int in_color_matrix: None
        :param int out_color_matrix: None
        :param int in_range: None
        :param int out_range: None
        :param int in_v_chr_pos: None
        :param int in_h_chr_pos: None
        :param int out_v_chr_pos: None
        :param int out_h_chr_pos: None
        :param int force_original_aspect_ratio: None
        :param int force_divisible_by: None
        :param float param0: None
        :param float param1: None
        :param int eval: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#scale

        """
        filter_node = FilterNode(
            name="scale",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "w": w,
                "h": h,
                "flags": flags,
                "interl": interl,
                "size": size,
                "in_color_matrix": in_color_matrix,
                "out_color_matrix": out_color_matrix,
                "in_range": in_range,
                "out_range": out_range,
                "in_v_chr_pos": in_v_chr_pos,
                "in_h_chr_pos": in_h_chr_pos,
                "out_v_chr_pos": out_v_chr_pos,
                "out_h_chr_pos": out_h_chr_pos,
                "force_original_aspect_ratio": force_original_aspect_ratio,
                "force_divisible_by": force_divisible_by,
                "param0": param0,
                "param1": param1,
                "eval": eval,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def scale2ref(
        self,
        _ref: "VideoStream",
        *,
        w: str,
        h: str,
        flags: str | DefaultStr = DefaultStr(""),
        interl: bool | DefaultInt = DefaultInt(0),
        size: str,
        in_color_matrix: int
        | Literal["auto", "bt601", "bt470", "smpte170m", "bt709", "fcc", "smpte240m", "bt2020"]
        | DefaultStr = DefaultStr("auto"),
        out_color_matrix: int
        | Literal["auto", "bt601", "bt470", "smpte170m", "bt709", "fcc", "smpte240m", "bt2020"]
        | DefaultStr = DefaultStr("AVCOL_SPC_UNSPECIFIED"),
        in_range: int
        | Literal["auto", "unknown", "full", "limited", "jpeg", "mpeg", "tv", "pc"]
        | DefaultStr = DefaultStr("auto"),
        out_range: int
        | Literal["auto", "unknown", "full", "limited", "jpeg", "mpeg", "tv", "pc"]
        | DefaultStr = DefaultStr("auto"),
        in_v_chr_pos: int | DefaultInt = DefaultInt(-513),
        in_h_chr_pos: int | DefaultInt = DefaultInt(-513),
        out_v_chr_pos: int | DefaultInt = DefaultInt(-513),
        out_h_chr_pos: int | DefaultInt = DefaultInt(-513),
        force_original_aspect_ratio: int
        | Literal["disable", "decrease", "increase"]
        | DefaultStr = DefaultStr("disable"),
        force_divisible_by: int | DefaultInt = DefaultInt(1),
        param0: float | DefaultFloat = DefaultFloat(1.7976931348623157e308),
        param1: float | DefaultFloat = DefaultFloat(1.7976931348623157e308),
        eval: int | DefaultStr = DefaultStr("EVAL_MODE_INIT"),
        **kwargs: Any,
    ) -> tuple["VideoStream", "VideoStream",]:
        """

        11.218 scale2ref
        Scale (resize) the input video, based on a reference video.

        See the scale filter for available options, scale2ref supports the same but
        uses the reference video instead of the main input as basis. scale2ref also
        supports the following additional constants for the w and
        h options:

        Parameters:
        ----------

        :param str w: None
        :param str h: None
        :param str flags: None
        :param bool interl: None
        :param str size: None
        :param int in_color_matrix: None
        :param int out_color_matrix: None
        :param int in_range: None
        :param int out_range: None
        :param int in_v_chr_pos: None
        :param int in_h_chr_pos: None
        :param int out_v_chr_pos: None
        :param int out_h_chr_pos: None
        :param int force_original_aspect_ratio: None
        :param int force_divisible_by: None
        :param float param0: None
        :param float param1: None
        :param int eval: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#scale2ref

        """
        filter_node = FilterNode(
            name="scale2ref",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video, StreamType.video],
            inputs=[
                self,
                _ref,
            ],
            kwargs={
                "w": w,
                "h": h,
                "flags": flags,
                "interl": interl,
                "size": size,
                "in_color_matrix": in_color_matrix,
                "out_color_matrix": out_color_matrix,
                "in_range": in_range,
                "out_range": out_range,
                "in_v_chr_pos": in_v_chr_pos,
                "in_h_chr_pos": in_h_chr_pos,
                "out_v_chr_pos": out_v_chr_pos,
                "out_h_chr_pos": out_h_chr_pos,
                "force_original_aspect_ratio": force_original_aspect_ratio,
                "force_divisible_by": force_divisible_by,
                "param0": param0,
                "param1": param1,
                "eval": eval,
            }
            | kwargs,
        )
        return (
            filter_node.video(0),
            filter_node.video(1),
        )

    def scale2ref_npp(
        self,
        _ref: "VideoStream",
        *,
        w: str,
        h: str,
        format: str | DefaultStr = DefaultStr("same"),
        s: str,
        interp_algo: int
        | Literal[
            "nn", "linear", "cubic", "cubic2p_bspline", "cubic2p_catmullrom", "cubic2p_b05c03", "super", "lanczos"
        ]
        | DefaultStr = DefaultStr("cubic"),
        force_original_aspect_ratio: int
        | Literal["disable", "decrease", "increase"]
        | DefaultStr = DefaultStr("disable"),
        force_divisible_by: int | DefaultInt = DefaultInt(1),
        eval: int | Literal["init", "frame"] | DefaultStr = DefaultStr("init"),
        **kwargs: Any,
    ) -> tuple["VideoStream", "VideoStream",]:
        """

        11.219 scale2ref_npp
        Use the NVIDIA Performance Primitives (libnpp) to scale (resize) the input
        video, based on a reference video.

        See the scale_npp filter for available options, scale2ref_npp supports the same
        but uses the reference video instead of the main input as basis. scale2ref_npp
        also supports the following additional constants for the w and
        h options:

        Parameters:
        ----------

        :param str w: None
        :param str h: None
        :param str format: None
        :param str s: None
        :param int interp_algo: None
        :param int force_original_aspect_ratio: None
        :param int force_divisible_by: None
        :param int eval: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#scale2ref_005fnpp

        """
        filter_node = FilterNode(
            name="scale2ref_npp",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video, StreamType.video],
            inputs=[
                self,
                _ref,
            ],
            kwargs={
                "w": w,
                "h": h,
                "format": format,
                "s": s,
                "interp_algo": interp_algo,
                "force_original_aspect_ratio": force_original_aspect_ratio,
                "force_divisible_by": force_divisible_by,
                "eval": eval,
            }
            | kwargs,
        )
        return (
            filter_node.video(0),
            filter_node.video(1),
        )

    def scale_cuda(
        self,
        *,
        w: str | DefaultStr = DefaultStr("iw"),
        h: str | DefaultStr = DefaultStr("ih"),
        interp_algo: int
        | Literal["nearest", "bilinear", "bicubic", "lanczos"]
        | DefaultStr = DefaultStr("INTERP_ALGO_DEFAULT"),
        format: str | DefaultStr = DefaultStr("AV_PIX_FMT_NONE"),
        passthrough: bool | DefaultInt = DefaultInt(1),
        param: float | DefaultStr = DefaultStr("999999.0f"),
        force_original_aspect_ratio: int
        | Literal["disable", "decrease", "increase"]
        | DefaultStr = DefaultStr("disable"),
        force_divisible_by: int | DefaultInt = DefaultInt(1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.216 scale_cuda
        Scale (resize) and convert (pixel format) the input video, using accelerated CUDA kernels.
        Setting the output width and height works in the same way as for the scale filter.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str w: Set the output video dimension expression. Default value is the input dimension. Allows for the same expressions as the scale filter.
        :param str h: Set the output video dimension expression. Default value is the input dimension. Allows for the same expressions as the scale filter.
        :param int interp_algo: Sets the algorithm used for scaling: nearest Nearest neighbour Used by default if input parameters match the desired output. bilinear Bilinear bicubic Bicubic This is the default. lanczos Lanczos
        :param str format: Controls the output pixel format. By default, or if none is specified, the input pixel format is used. The filter does not support converting between YUV and RGB pixel formats.
        :param bool passthrough: If set to 0, every frame is processed, even if no conversion is necessary. This mode can be useful to use the filter as a buffer for a downstream frame-consumer that exhausts the limited decoder frame pool. If set to 1, frames are passed through as-is if they match the desired output parameters. This is the default behaviour.
        :param float param: Algorithm-Specific parameter. Affects the curves of the bicubic algorithm.
        :param int force_original_aspect_ratio: Work the same as the identical scale filter options.
        :param int force_divisible_by: Work the same as the identical scale filter options.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#scale_005fcuda

        """
        filter_node = FilterNode(
            name="scale_cuda",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "w": w,
                "h": h,
                "interp_algo": interp_algo,
                "format": format,
                "passthrough": passthrough,
                "param": param,
                "force_original_aspect_ratio": force_original_aspect_ratio,
                "force_divisible_by": force_divisible_by,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def scale_npp(
        self,
        *,
        w: str,
        h: str,
        format: str | DefaultStr = DefaultStr("same"),
        s: str,
        interp_algo: int
        | Literal[
            "nn", "linear", "cubic", "cubic2p_bspline", "cubic2p_catmullrom", "cubic2p_b05c03", "super", "lanczos"
        ]
        | DefaultStr = DefaultStr("cubic"),
        force_original_aspect_ratio: int
        | Literal["disable", "decrease", "increase"]
        | DefaultStr = DefaultStr("disable"),
        force_divisible_by: int | DefaultInt = DefaultInt(1),
        eval: int | Literal["init", "frame"] | DefaultStr = DefaultStr("init"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.217 scale_npp
        Use the NVIDIA Performance Primitives (libnpp) to perform scaling and/or pixel
        format conversion on CUDA video frames. Setting the output width and height
        works in the same way as for the scale filter.

        The following additional options are accepted:

        The values of the w and h options are expressions
        containing the following constants:

        Parameters:
        ----------

        :param str w: None
        :param str h: None
        :param str format: The pixel format of the output CUDA frames. If set to the string "same" (the default), the input format will be kept. Note that automatic format negotiation and conversion is not yet supported for hardware frames
        :param str s: None
        :param int interp_algo: The interpolation algorithm used for resizing. One of the following: nn Nearest neighbour. linear cubic cubic2p_bspline 2-parameter cubic (B=1, C=0) cubic2p_catmullrom 2-parameter cubic (B=0, C=1/2) cubic2p_b05c03 2-parameter cubic (B=1/2, C=3/10) super Supersampling lanczos
        :param int force_original_aspect_ratio: Enable decreasing or increasing output video width or height if necessary to keep the original aspect ratio. Possible values: ‘disable’ Scale the video as specified and disable this feature. ‘decrease’ The output video dimensions will automatically be decreased if needed. ‘increase’ The output video dimensions will automatically be increased if needed. One useful instance of this option is that when you know a specific device’s maximum allowed resolution, you can use this to limit the output video to that, while retaining the aspect ratio. For example, device A allows 1280x720 playback, and your video is 1920x800. Using this option (set it to decrease) and specifying 1280x720 to the command line makes the output 1280x533. Please note that this is a different thing than specifying -1 for w or h, you still need to specify the output resolution for this option to work.
        :param int force_divisible_by: Ensures that both the output dimensions, width and height, are divisible by the given integer when used together with force_original_aspect_ratio. This works similar to using -n in the w and h options. This option respects the value set for force_original_aspect_ratio, increasing or decreasing the resolution accordingly. The video’s aspect ratio may be slightly modified. This option can be handy if you need to have a video fit within or exceed a defined resolution using force_original_aspect_ratio but also have encoder restrictions on width or height divisibility.
        :param int eval: Specify when to evaluate width and height expression. It accepts the following values: ‘init’ Only evaluate expressions once during the filter initialization or when a command is processed. ‘frame’ Evaluate expressions for each incoming frame.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#scale_005fnpp

        """
        filter_node = FilterNode(
            name="scale_npp",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "w": w,
                "h": h,
                "format": format,
                "s": s,
                "interp_algo": interp_algo,
                "force_original_aspect_ratio": force_original_aspect_ratio,
                "force_divisible_by": force_divisible_by,
                "eval": eval,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def scale_vt(
        self,
        *,
        w: str | DefaultStr = DefaultStr("iw"),
        h: str | DefaultStr = DefaultStr("ih"),
        color_matrix: str,
        color_primaries: str,
        color_transfer: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.220 scale_vt
        Scale and convert the color parameters using VTPixelTransferSession.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str w: Set the output video dimension expression. Default value is the input dimension.
        :param str h: Set the output video dimension expression. Default value is the input dimension.
        :param str color_matrix: Set the output colorspace matrix.
        :param str color_primaries: Set the output color primaries.
        :param str color_transfer: Set the output transfer characteristics.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#scale_005fvt

        """
        filter_node = FilterNode(
            name="scale_vt",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "w": w,
                "h": h,
                "color_matrix": color_matrix,
                "color_primaries": color_primaries,
                "color_transfer": color_transfer,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def scdet(
        self,
        *,
        threshold: float | DefaultFloat = DefaultFloat(10.0),
        sc_pass: bool | DefaultStr = DefaultStr(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.223 scdet
        Detect video scene change.

        This filter sets frame metadata with mafd between frame, the scene score, and
        forward the frame to the next filter, so they can use these metadata to detect
        scene change or others.

        In addition, this filter logs a message and sets frame metadata when it detects
        a scene change by threshold.

        lavfi.scd.mafd metadata keys are set with mafd for every frame.

        lavfi.scd.score metadata keys are set with scene change score for every frame
        to detect scene change.

        lavfi.scd.time metadata keys are set with current filtered frame time which
        detect scene change with threshold.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float threshold: Set the scene change detection threshold as a percentage of maximum change. Good values are in the [8.0, 14.0] range. The range for threshold is [0., 100.]. Default value is 10..
        :param bool sc_pass: Set the flag to pass scene change frames to the next filter. Default value is 0 You can enable it if you want to get snapshot of scene change frames only.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#scdet

        """
        filter_node = FilterNode(
            name="scdet",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "threshold": threshold,
                "sc_pass": sc_pass,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def scharr(
        self,
        *,
        planes: int | DefaultInt = DefaultInt(15),
        scale: float | DefaultFloat = DefaultFloat(1.0),
        delta: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.221 scharr
        Apply scharr operator to input video stream.

        The filter accepts the following option:

        Parameters:
        ----------

        :param int planes: Set which planes will be processed, unprocessed planes will be copied. By default value 0xf, all planes will be processed.
        :param float scale: Set value which will be multiplied with filtered result.
        :param float delta: Set value which will be added to filtered result.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#scharr

        """
        filter_node = FilterNode(
            name="scharr",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "planes": planes,
                "scale": scale,
                "delta": delta,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def scroll(
        self,
        *,
        horizontal: float | DefaultFloat = DefaultFloat(0.0),
        vertical: float | DefaultFloat = DefaultFloat(0.0),
        hpos: float | DefaultFloat = DefaultFloat(0.0),
        vpos: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.222 scroll
        Scroll input video horizontally and/or vertically by constant speed.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float horizontal: Set the horizontal scrolling speed. Default is 0. Allowed range is from -1 to 1. Negative values changes scrolling direction.
        :param float vertical: Set the vertical scrolling speed. Default is 0. Allowed range is from -1 to 1. Negative values changes scrolling direction.
        :param float hpos: Set the initial horizontal scrolling position. Default is 0. Allowed range is from 0 to 1.
        :param float vpos: Set the initial vertical scrolling position. Default is 0. Allowed range is from 0 to 1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#scroll

        """
        filter_node = FilterNode(
            name="scroll",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "horizontal": horizontal,
                "vertical": vertical,
                "hpos": hpos,
                "vpos": vpos,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def segment(self, *, timestamps: str, frames: str, **kwargs: Any) -> FilterNode:
        """

        18.16 segment, asegment
        Split single input stream into multiple streams.

        This filter does opposite of concat filters.

        segment works on video frames, asegment on audio samples.

        This filter accepts the following options:


        In all cases, prefixing an each segment with ’+’ will make it relative to the
        previous segment.

        Parameters:
        ----------

        :param str timestamps: Timestamps of output segments separated by ’|’. The first segment will run from the beginning of the input stream. The last segment will run until the end of the input stream
        :param str frames: Exact frame/sample count to split the segments.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#segment_002c-asegment

        """
        filter_node = FilterNode(
            name="segment",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video] * len((timestamps or frames).split("|")),
            inputs=[
                self,
            ],
            kwargs={
                "timestamps": timestamps,
                "frames": frames,
            }
            | kwargs,
        )

        return filter_node

    def select(
        self, *, expr: str | DefaultStr = DefaultStr("1"), outputs: int | DefaultInt = DefaultInt(1), **kwargs: Any
    ) -> FilterNode:
        """

        18.17 select, aselect
        Select frames to pass in output.

        This filter accepts the following options:


        The expression can contain the following constants:


        The default value of the select expression is "1".

        Parameters:
        ----------

        :param str expr: Set expression, which is evaluated for each input frame. If the expression is evaluated to zero, the frame is discarded. If the evaluation result is negative or NaN, the frame is sent to the first output; otherwise it is sent to the output with index ceil(val)-1, assuming that the input index starts from 0. For example a value of 1.2 corresponds to the output with index ceil(1.2)-1 = 2-1 = 1, that is the second output.
        :param int outputs: Set the number of outputs. The output to which to send the selected frame is based on the result of the evaluation. Default value is 1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#select_002c-aselect

        """
        filter_node = FilterNode(
            name="select",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video] * outputs,
            inputs=[
                self,
            ],
            kwargs={
                "expr": expr,
                "outputs": outputs,
            }
            | kwargs,
        )

        return filter_node

    def selectivecolor(
        self,
        *,
        correction_method: int | Literal["absolute", "relative"] | DefaultStr = DefaultStr("absolute"),
        reds: str,
        yellows: str,
        greens: str,
        cyans: str,
        blues: str,
        magentas: str,
        whites: str,
        neutrals: str,
        blacks: str,
        psfile: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.224 selectivecolor
        Adjust cyan, magenta, yellow and black (CMYK) to certain ranges of colors (such
        as "reds", "yellows", "greens", "cyans", ...). The adjustment range is defined
        by the "purity" of the color (that is, how saturated it already is).

        This filter is similar to the Adobe Photoshop Selective Color tool.

        The filter accepts the following options:


        All the adjustment settings (reds, yellows, ...) accept up to
        4 space separated floating point adjustment values in the [-1,1] range,
        respectively to adjust the amount of cyan, magenta, yellow and black for the
        pixels of its range.

        Parameters:
        ----------

        :param int correction_method: Select color correction method. Available values are: ‘absolute’ Specified adjustments are applied "as-is" (added/subtracted to original pixel component value). ‘relative’ Specified adjustments are relative to the original component value. Default is absolute.
        :param str reds: Adjustments for red pixels (pixels where the red component is the maximum)
        :param str yellows: Adjustments for yellow pixels (pixels where the blue component is the minimum)
        :param str greens: Adjustments for green pixels (pixels where the green component is the maximum)
        :param str cyans: Adjustments for cyan pixels (pixels where the red component is the minimum)
        :param str blues: Adjustments for blue pixels (pixels where the blue component is the maximum)
        :param str magentas: Adjustments for magenta pixels (pixels where the green component is the minimum)
        :param str whites: Adjustments for white pixels (pixels where all components are greater than 128)
        :param str neutrals: Adjustments for all pixels except pure black and pure white
        :param str blacks: Adjustments for black pixels (pixels where all components are lesser than 128)
        :param str psfile: Specify a Photoshop selective color file (.asv) to import the settings from.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#selectivecolor

        """
        filter_node = FilterNode(
            name="selectivecolor",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "correction_method": correction_method,
                "reds": reds,
                "yellows": yellows,
                "greens": greens,
                "cyans": cyans,
                "blues": blues,
                "magentas": magentas,
                "whites": whites,
                "neutrals": neutrals,
                "blacks": blacks,
                "psfile": psfile,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def sendcmd(self, *, commands: str, filename: str, **kwargs: Any) -> "VideoStream":
        """

        18.18 sendcmd, asendcmd
        Send commands to filters in the filtergraph.

        These filters read commands to be sent to other filters in the
        filtergraph.

        sendcmd must be inserted between two video filters,
        asendcmd must be inserted between two audio filters, but apart
        from that they act the same way.

        The specification of commands can be provided in the filter arguments
        with the commands option, or in a file specified by the
        filename option.

        These filters accept the following options:

        Parameters:
        ----------

        :param str commands: Set the commands to be read and sent to the other filters.
        :param str filename: Set the filename of the commands to be read and sent to the other filters.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#sendcmd_002c-asendcmd

        """
        filter_node = FilterNode(
            name="sendcmd",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "commands": commands,
                "filename": filename,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def separatefields(self, **kwargs: Any) -> "VideoStream":
        """

        11.225 separatefields
        The separatefields takes a frame-based video input and splits
        each frame into its components fields, producing a new half height clip
        with twice the frame rate and twice the frame count.

        This filter use field-dominance information in frame to decide which
        of each pair of fields to place first in the output.
        If it gets it wrong use setfield filter before separatefields filter.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#separatefields

        """
        filter_node = FilterNode(
            name="separatefields",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def setdar(
        self, *, dar: str | DefaultStr = DefaultStr("0"), max: int | DefaultInt = DefaultInt(100), **kwargs: Any
    ) -> "VideoStream":
        """

        11.226 setdar, setsar
        The setdar filter sets the Display Aspect Ratio for the filter
        output video.

        This is done by changing the specified Sample (aka Pixel) Aspect
        Ratio, according to the following equation:

        DAR = HORIZONTAL_RESOLUTION / VERTICAL_RESOLUTION * SAR

        Keep in mind that the setdar filter does not modify the pixel
        dimensions of the video frame. Also, the display aspect ratio set by
        this filter may be changed by later filters in the filterchain,
        e.g. in case of scaling or if another "setdar" or a "setsar" filter is
        applied.

        The setsar filter sets the Sample (aka Pixel) Aspect Ratio for
        the filter output video.

        Note that as a consequence of the application of this filter, the
        output display aspect ratio will change according to the equation
        above.

        Keep in mind that the sample aspect ratio set by the setsar
        filter may be changed by later filters in the filterchain, e.g. if
        another "setsar" or a "setdar" filter is applied.

        It accepts the following parameters:


        The parameter sar is an expression containing the following constants:

        Parameters:
        ----------

        :param str dar: Set the aspect ratio used by the filter. The parameter can be a floating point number string, or an expression. If the parameter is not specified, the value "0" is assumed, meaning that the same input value is used.
        :param int max: Set the maximum integer value to use for expressing numerator and denominator when reducing the expressed aspect ratio to a rational. Default value is 100.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#setdar_002c-setsar

        """
        filter_node = FilterNode(
            name="setdar",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dar": dar,
                "max": max,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def setfield(
        self, *, mode: int | Literal["auto", "bff", "tff", "prog"] | DefaultStr = DefaultStr("auto"), **kwargs: Any
    ) -> "VideoStream":
        """

        11.227 setfield
        Force field for the output video frame.

        The setfield filter marks the interlace type field for the
        output frames. It does not change the input frame, but only sets the
        corresponding property, which affects how the frame is treated by
        following filters (e.g. fieldorder or yadif).

        The filter accepts the following options:

        Parameters:
        ----------

        :param int mode: Available values are: ‘auto’ Keep the same field property. ‘bff’ Mark the frame as bottom-field-first. ‘tff’ Mark the frame as top-field-first. ‘prog’ Mark the frame as progressive.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#setfield

        """
        filter_node = FilterNode(
            name="setfield",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def setparams(
        self,
        *,
        field_mode: int | Literal["auto", "bff", "tff", "prog"] | DefaultStr = DefaultStr("auto"),
        range: int
        | Literal["auto", "unspecified", "unknown", "limited", "tv", "mpeg", "full", "pc", "jpeg"]
        | DefaultStr = DefaultStr("auto"),
        color_primaries: int
        | Literal[
            "auto",
            "bt709",
            "unknown",
            "bt470m",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "film",
            "bt2020",
            "smpte428",
            "smpte431",
            "smpte432",
            "jedec-p22",
            "ebu3213",
        ]
        | DefaultStr = DefaultStr("auto"),
        color_trc: int
        | Literal[
            "auto",
            "bt709",
            "unknown",
            "bt470m",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "linear",
            "log100",
            "log316",
            "iec61966-2-4",
            "bt1361e",
            "iec61966-2-1",
            "bt2020-10",
            "bt2020-12",
            "smpte2084",
            "smpte428",
            "arib-std-b67",
        ]
        | DefaultStr = DefaultStr("auto"),
        colorspace: int
        | Literal[
            "auto",
            "gbr",
            "bt709",
            "unknown",
            "fcc",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "ycgco",
            "bt2020nc",
            "bt2020c",
            "smpte2085",
            "chroma-derived-nc",
            "chroma-derived-c",
            "ictcp",
        ]
        | DefaultStr = DefaultStr("auto"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.228 setparams
        Force frame parameter for the output video frame.

        The setparams filter marks interlace and color range for the
        output frames. It does not change the input frame, but only sets the
        corresponding property, which affects how the frame is treated by
        filters/encoders.

        Parameters:
        ----------

        :param int field_mode: Available values are: ‘auto’ Keep the same field property (default). ‘bff’ Mark the frame as bottom-field-first. ‘tff’ Mark the frame as top-field-first. ‘prog’ Mark the frame as progressive.
        :param int range: Available values are: ‘auto’ Keep the same color range property (default). ‘unspecified, unknown’ Mark the frame as unspecified color range. ‘limited, tv, mpeg’ Mark the frame as limited range. ‘full, pc, jpeg’ Mark the frame as full range.
        :param int color_primaries: Set the color primaries. Available values are: ‘auto’ Keep the same color primaries property (default). ‘bt709’ ‘unknown’ ‘bt470m’ ‘bt470bg’ ‘smpte170m’ ‘smpte240m’ ‘film’ ‘bt2020’ ‘smpte428’ ‘smpte431’ ‘smpte432’ ‘jedec-p22’
        :param int color_trc: Set the color transfer. Available values are: ‘auto’ Keep the same color trc property (default). ‘bt709’ ‘unknown’ ‘bt470m’ ‘bt470bg’ ‘smpte170m’ ‘smpte240m’ ‘linear’ ‘log100’ ‘log316’ ‘iec61966-2-4’ ‘bt1361e’ ‘iec61966-2-1’ ‘bt2020-10’ ‘bt2020-12’ ‘smpte2084’ ‘smpte428’ ‘arib-std-b67’
        :param int colorspace: Set the colorspace. Available values are: ‘auto’ Keep the same colorspace property (default). ‘gbr’ ‘bt709’ ‘unknown’ ‘fcc’ ‘bt470bg’ ‘smpte170m’ ‘smpte240m’ ‘ycgco’ ‘bt2020nc’ ‘bt2020c’ ‘smpte2085’ ‘chroma-derived-nc’ ‘chroma-derived-c’ ‘ictcp’

        Ref: https://ffmpeg.org/ffmpeg-filters.html#setparams

        """
        filter_node = FilterNode(
            name="setparams",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "field_mode": field_mode,
                "range": range,
                "color_primaries": color_primaries,
                "color_trc": color_trc,
                "colorspace": colorspace,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def setpts(self, *, expr: str | DefaultStr = DefaultStr("PTS"), **kwargs: Any) -> "VideoStream":
        """

        18.19 setpts, asetpts
        Change the PTS (presentation timestamp) of the input frames.

        setpts works on video frames, asetpts on audio frames.

        This filter accepts the following options:


        The expression is evaluated through the eval API and can contain the following
        constants:

        Parameters:
        ----------

        :param str expr: The expression which is evaluated for each frame to construct its timestamp.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#setpts_002c-asetpts

        """
        filter_node = FilterNode(
            name="setpts",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "expr": expr,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def setrange(
        self,
        *,
        range: int
        | Literal["auto", "unspecified", "unknown", "limited", "tv", "mpeg", "full", "pc", "jpeg"]
        | DefaultStr = DefaultStr("auto"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        18.20 setrange
        Force color range for the output video frame.

        The setrange filter marks the color range property for the
        output frames. It does not change the input frame, but only sets the
        corresponding property, which affects how the frame is treated by
        following filters.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int range: Available values are: ‘auto’ Keep the same color range property. ‘unspecified, unknown’ Set the color range as unspecified. ‘limited, tv, mpeg’ Set the color range as limited. ‘full, pc, jpeg’ Set the color range as full.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#setrange

        """
        filter_node = FilterNode(
            name="setrange",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "range": range,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def setsar(
        self, *, sar: str | DefaultStr = DefaultStr("0"), max: int | DefaultInt = DefaultInt(100), **kwargs: Any
    ) -> "VideoStream":
        """

        11.226 setdar, setsar
        The setdar filter sets the Display Aspect Ratio for the filter
        output video.

        This is done by changing the specified Sample (aka Pixel) Aspect
        Ratio, according to the following equation:

        DAR = HORIZONTAL_RESOLUTION / VERTICAL_RESOLUTION * SAR

        Keep in mind that the setdar filter does not modify the pixel
        dimensions of the video frame. Also, the display aspect ratio set by
        this filter may be changed by later filters in the filterchain,
        e.g. in case of scaling or if another "setdar" or a "setsar" filter is
        applied.

        The setsar filter sets the Sample (aka Pixel) Aspect Ratio for
        the filter output video.

        Note that as a consequence of the application of this filter, the
        output display aspect ratio will change according to the equation
        above.

        Keep in mind that the sample aspect ratio set by the setsar
        filter may be changed by later filters in the filterchain, e.g. if
        another "setsar" or a "setdar" filter is applied.

        It accepts the following parameters:


        The parameter sar is an expression containing the following constants:

        Parameters:
        ----------

        :param str sar: Set the aspect ratio used by the filter. The parameter can be a floating point number string, or an expression. If the parameter is not specified, the value "0" is assumed, meaning that the same input value is used.
        :param int max: Set the maximum integer value to use for expressing numerator and denominator when reducing the expressed aspect ratio to a rational. Default value is 100.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#setdar_002c-setsar

        """
        filter_node = FilterNode(
            name="setsar",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "sar": sar,
                "max": max,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def settb(self, *, expr: str | DefaultStr = DefaultStr("intb"), **kwargs: Any) -> "VideoStream":
        """

        18.21 settb, asettb
        Set the timebase to use for the output frames timestamps.
        It is mainly useful for testing timebase configuration.

        It accepts the following parameters:


        The value for tb is an arithmetic expression representing a
        rational. The expression can contain the constants "AVTB" (the default
        timebase), "intb" (the input timebase) and "sr" (the sample rate,
        audio only). Default value is "intb".

        Parameters:
        ----------

        :param str expr: The expression which is evaluated into the output timebase.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#settb_002c-asettb

        """
        filter_node = FilterNode(
            name="settb",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "expr": expr,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def sharpen_npp(
        self, *, border_type: int | Literal["replicate"] | DefaultStr = DefaultStr("replicate"), **kwargs: Any
    ) -> "VideoStream":
        """

        11.229 sharpen_npp
        Use the NVIDIA Performance Primitives (libnpp) to perform image sharpening with
        border control.

        The following additional options are accepted:

        Parameters:
        ----------

        :param int border_type: Type of sampling to be used ad frame borders. One of the following: replicate Replicate pixel values.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#sharpen_005fnpp

        """
        filter_node = FilterNode(
            name="sharpen_npp",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "border_type": border_type,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def shear(
        self,
        *,
        shx: float | DefaultFloat = DefaultFloat(0.0),
        shy: float | DefaultFloat = DefaultFloat(0.0),
        fillcolor: str | DefaultStr = DefaultStr("black"),
        interp: int | Literal["nearest", "bilinear"] | DefaultStr = DefaultStr("bilinear"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.230 shear
        Apply shear transform to input video.

        This filter supports the following options:

        Parameters:
        ----------

        :param float shx: Shear factor in X-direction. Default value is 0. Allowed range is from -2 to 2.
        :param float shy: Shear factor in Y-direction. Default value is 0. Allowed range is from -2 to 2.
        :param str fillcolor: Set the color used to fill the output area not covered by the transformed video. For the general syntax of this option, check the (ffmpeg-utils)"Color" section in the ffmpeg-utils manual. If the special value "none" is selected then no background is printed (useful for example if the background is never shown). Default value is "black".
        :param int interp: Set interpolation type. Can be bilinear or nearest. Default is bilinear.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#shear

        """
        filter_node = FilterNode(
            name="shear",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "shx": shx,
                "shy": shy,
                "fillcolor": fillcolor,
                "interp": interp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def showinfo(self, *, checksum: bool | DefaultInt = DefaultInt(1), **kwargs: Any) -> "VideoStream":
        """

        11.231 showinfo
        Show a line containing various information for each input video frame.
        The input video is not modified.

        This filter supports the following options:


        The shown line contains a sequence of key/value pairs of the form
        key:value.

        The following values are shown in the output:

        Parameters:
        ----------

        :param bool checksum: Calculate checksums of each plane. By default enabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#showinfo

        """
        filter_node = FilterNode(
            name="showinfo",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "checksum": checksum,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def showpalette(self, *, s: int | DefaultInt = DefaultInt(30), **kwargs: Any) -> "VideoStream":
        """

        11.232 showpalette
        Displays the 256 colors palette of each frame. This filter is only relevant for
        pal8 pixel format frames.

        It accepts the following option:

        Parameters:
        ----------

        :param int s: Set the size of the box used to represent one palette color entry. Default is 30 (for a 30x30 pixel box).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#showpalette

        """
        filter_node = FilterNode(
            name="showpalette",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "s": s,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def shuffleframes(self, *, mapping: str | DefaultStr = DefaultStr("0"), **kwargs: Any) -> "VideoStream":
        """

        11.233 shuffleframes
        Reorder and/or duplicate and/or drop video frames.

        It accepts the following parameters:


        The first frame has the index 0. The default is to keep the input unchanged.

        Parameters:
        ----------

        :param str mapping: Set the destination indexes of input frames. This is space or ’|’ separated list of indexes that maps input frames to output frames. Number of indexes also sets maximal value that each index may have. ’-1’ index have special meaning and that is to drop frame.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#shuffleframes

        """
        filter_node = FilterNode(
            name="shuffleframes",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mapping": mapping,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def shufflepixels(
        self,
        *,
        direction: int | Literal["forward", "inverse"] | DefaultStr = DefaultStr("forward"),
        mode: int | Literal["horizontal", "vertical", "block"] | DefaultStr = DefaultStr("horizontal"),
        width: int | DefaultInt = DefaultInt(10),
        height: int | DefaultInt = DefaultInt(10),
        seed: int | DefaultInt = DefaultInt(-1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.234 shufflepixels
        Reorder pixels in video frames.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int direction: Set shuffle direction. Can be forward or inverse direction. Default direction is forward.
        :param int mode: Set shuffle mode. Can be horizontal, vertical or block mode.
        :param int width: Set shuffle block_size. In case of horizontal shuffle mode only width part of size is used, and in case of vertical shuffle mode only height part of size is used.
        :param int height: Set shuffle block_size. In case of horizontal shuffle mode only width part of size is used, and in case of vertical shuffle mode only height part of size is used.
        :param int seed: Set random seed used with shuffling pixels. Mainly useful to set to be able to reverse filtering process to get original input. For example, to reverse forward shuffle you need to use same parameters and exact same seed and to set direction to inverse.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#shufflepixels

        """
        filter_node = FilterNode(
            name="shufflepixels",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "direction": direction,
                "mode": mode,
                "width": width,
                "height": height,
                "seed": seed,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def shuffleplanes(
        self,
        *,
        map0: int | DefaultInt = DefaultInt(0),
        map1: int | DefaultInt = DefaultInt(1),
        map2: int | DefaultInt = DefaultInt(2),
        map3: int | DefaultInt = DefaultInt(3),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.235 shuffleplanes
        Reorder and/or duplicate video planes.

        It accepts the following parameters:


        The first plane has the index 0. The default is to keep the input unchanged.

        Parameters:
        ----------

        :param int map0: The index of the input plane to be used as the first output plane.
        :param int map1: The index of the input plane to be used as the second output plane.
        :param int map2: The index of the input plane to be used as the third output plane.
        :param int map3: The index of the input plane to be used as the fourth output plane.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#shuffleplanes

        """
        filter_node = FilterNode(
            name="shuffleplanes",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "map0": map0,
                "map1": map1,
                "map2": map2,
                "map3": map3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def sidedata(
        self,
        *,
        mode: int | Literal["select", "delete"] | DefaultStr = DefaultStr(0),
        type: int
        | Literal[
            "PANSCAN",
            "A53_CC",
            "STEREO3D",
            "MATRIXENCODING",
            "DOWNMIX_INFO",
            "REPLAYGAIN",
            "DISPLAYMATRIX",
            "AFD",
            "MOTION_VECTORS",
            "SKIP_SAMPLES",
            "AUDIO_SERVICE_TYPE",
            "MASTERING_DISPLAY_METADATA",
            "GOP_TIMECODE",
            "SPHERICAL",
            "CONTENT_LIGHT_LEVEL",
            "ICC_PROFILE",
            "S12M_TIMECOD",
            "DYNAMIC_HDR_PLUS",
            "REGIONS_OF_INTEREST",
            "DETECTION_BOUNDING_BOXES",
            "SEI_UNREGISTERED",
        ]
        | DefaultStr = DefaultStr(-1),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        18.31 sidedata, asidedata
        Delete frame side data, or select frames based on it.

        This filter accepts the following options:

        Parameters:
        ----------

        :param int mode: Set mode of operation of the filter. Can be one of the following: ‘select’ Select every frame with side data of type. ‘delete’ Delete side data of type. If type is not set, delete all side data in the frame.
        :param int type: Set side data type used with all modes. Must be set for select mode. For the list of frame side data types, refer to the AVFrameSideDataType enum in libavutil/frame.h. For example, to choose AV_FRAME_DATA_PANSCAN side data, you must specify PANSCAN.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#sidedata_002c-asidedata

        """
        filter_node = FilterNode(
            name="sidedata",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "type": type,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def signalstats(
        self,
        *,
        stat: str | Literal["tout", "vrep", "brng"] | DefaultStr = DefaultStr(0),
        out: int | Literal["tout", "vrep", "brng"] | DefaultStr = DefaultStr("FILTER_NONE"),
        c: str | DefaultStr = DefaultStr("yellow"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.236 signalstats
        Evaluate various visual metrics that assist in determining issues associated
        with the digitization of analog video media.

        By default the filter will log these metadata values:


        The filter accepts the following options:

        Parameters:
        ----------

        :param str stat: stat specify an additional form of image analysis. out output video with the specified type of pixel highlighted. Both options accept the following values: ‘tout’ Identify temporal outliers pixels. A temporal outlier is a pixel unlike the neighboring pixels of the same field. Examples of temporal outliers include the results of video dropouts, head clogs, or tape tracking issues. ‘vrep’ Identify vertical line repetition. Vertical line repetition includes similar rows of pixels within a frame. In born-digital video vertical line repetition is common, but this pattern is uncommon in video digitized from an analog source. When it occurs in video that results from the digitization of an analog source it can indicate concealment from a dropout compensator. ‘brng’ Identify pixels that fall outside of legal broadcast range.
        :param int out: stat specify an additional form of image analysis. out output video with the specified type of pixel highlighted. Both options accept the following values: ‘tout’ Identify temporal outliers pixels. A temporal outlier is a pixel unlike the neighboring pixels of the same field. Examples of temporal outliers include the results of video dropouts, head clogs, or tape tracking issues. ‘vrep’ Identify vertical line repetition. Vertical line repetition includes similar rows of pixels within a frame. In born-digital video vertical line repetition is common, but this pattern is uncommon in video digitized from an analog source. When it occurs in video that results from the digitization of an analog source it can indicate concealment from a dropout compensator. ‘brng’ Identify pixels that fall outside of legal broadcast range.
        :param str c: Set the highlight color for the out option. The default color is yellow.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#signalstats

        """
        filter_node = FilterNode(
            name="signalstats",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "stat": stat,
                "out": out,
                "c": c,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def siti(self, *, print_summary: bool | DefaultInt = DefaultInt(0), **kwargs: Any) -> "VideoStream":
        """

        11.238 siti
        Calculate Spatial Information (SI) and Temporal Information (TI) scores for a video,
        as defined in ITU-T Rec. P.910 (11/21): Subjective video quality assessment methods
        for multimedia applications. Available PDF at https://www.itu.int/rec/T-REC-P.910-202111-S/en.
        Note that this is a legacy implementation that corresponds to a superseded recommendation.
        Refer to ITU-T Rec. P.910 (07/22) for the latest version: https://www.itu.int/rec/T-REC-P.910-202207-I/en

        It accepts the following option:

        Parameters:
        ----------

        :param bool print_summary: If set to 1, Summary statistics will be printed to the console. Default 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#siti

        """
        filter_node = FilterNode(
            name="siti",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "print_summary": print_summary,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def smartblur(
        self,
        *,
        luma_radius: float | DefaultFloat = DefaultFloat(1.0),
        luma_strength: float | DefaultFloat = DefaultFloat(1.0),
        luma_threshold: int | DefaultInt = DefaultInt(0),
        chroma_radius: float | DefaultStr = DefaultStr("0.1 -1"),
        chroma_strength: float | DefaultStr = DefaultStr("-1.0 -1"),
        chroma_threshold: int | DefaultStr = DefaultStr("-30 -1"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.239 smartblur
        Blur the input video without impacting the outlines.

        It accepts the following options:


        If a chroma option is not explicitly set, the corresponding luma value
        is set.

        Parameters:
        ----------

        :param float luma_radius: Set the luma radius. The option value must be a float number in the range [0.1,5.0] that specifies the variance of the gaussian filter used to blur the image (slower if larger). Default value is 1.0.
        :param float luma_strength: Set the luma strength. The option value must be a float number in the range [-1.0,1.0] that configures the blurring. A value included in [0.0,1.0] will blur the image whereas a value included in [-1.0,0.0] will sharpen the image. Default value is 1.0.
        :param int luma_threshold: Set the luma threshold used as a coefficient to determine whether a pixel should be blurred or not. The option value must be an integer in the range [-30,30]. A value of 0 will filter all the image, a value included in [0,30] will filter flat areas and a value included in [-30,0] will filter edges. Default value is 0.
        :param float chroma_radius: Set the chroma radius. The option value must be a float number in the range [0.1,5.0] that specifies the variance of the gaussian filter used to blur the image (slower if larger). Default value is luma_radius.
        :param float chroma_strength: Set the chroma strength. The option value must be a float number in the range [-1.0,1.0] that configures the blurring. A value included in [0.0,1.0] will blur the image whereas a value included in [-1.0,0.0] will sharpen the image. Default value is luma_strength.
        :param int chroma_threshold: Set the chroma threshold used as a coefficient to determine whether a pixel should be blurred or not. The option value must be an integer in the range [-30,30]. A value of 0 will filter all the image, a value included in [0,30] will filter flat areas and a value included in [-30,0] will filter edges. Default value is luma_threshold.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#smartblur

        """
        filter_node = FilterNode(
            name="smartblur",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "luma_radius": luma_radius,
                "luma_strength": luma_strength,
                "luma_threshold": luma_threshold,
                "chroma_radius": chroma_radius,
                "chroma_strength": chroma_strength,
                "chroma_threshold": chroma_threshold,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def sobel(
        self,
        *,
        planes: int | DefaultInt = DefaultInt(15),
        scale: float | DefaultFloat = DefaultFloat(1.0),
        delta: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.240 sobel
        Apply sobel operator to input video stream.

        The filter accepts the following option:

        Parameters:
        ----------

        :param int planes: Set which planes will be processed, unprocessed planes will be copied. By default value 0xf, all planes will be processed.
        :param float scale: Set value which will be multiplied with filtered result.
        :param float delta: Set value which will be added to filtered result.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#sobel

        """
        filter_node = FilterNode(
            name="sobel",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "planes": planes,
                "scale": scale,
                "delta": delta,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def sobel_opencl(
        self,
        *,
        planes: int | DefaultInt = DefaultInt(15),
        scale: float | DefaultFloat = DefaultFloat(1.0),
        delta: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.15 sobel_opencl
        Apply the Sobel operator (https://en.wikipedia.org/wiki/Sobel_operator) to input video stream.

        The filter accepts the following option:

        Parameters:
        ----------

        :param int planes: Set which planes to filter. Default value is 0xf, by which all planes are processed.
        :param float scale: Set value which will be multiplied with filtered result. Range is [0.0, 65535] and default value is 1.0.
        :param float delta: Set value which will be added to filtered result. Range is [-65535, 65535] and default value is 0.0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#sobel_005fopencl

        """
        filter_node = FilterNode(
            name="sobel_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "planes": planes,
                "scale": scale,
                "delta": delta,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def spectrumsynth(
        self,
        _phase: "VideoStream",
        *,
        sample_rate: int | DefaultInt = DefaultInt(44100),
        channels: int | DefaultInt = DefaultInt(1),
        scale: int | Literal["lin", "log"] | DefaultStr = DefaultStr("log"),
        slide: int | Literal["replace", "scroll", "fullframe", "rscroll"] | DefaultStr = DefaultStr("fullframe"),
        win_func: int
        | Literal[
            "rect",
            "bartlett",
            "hann",
            "hanning",
            "hamming",
            "blackman",
            "welch",
            "flattop",
            "bharris",
            "bnuttall",
            "bhann",
            "sine",
            "nuttall",
            "lanczos",
            "gauss",
            "tukey",
            "dolph",
            "cauchy",
            "parzen",
            "poisson",
            "bohman",
            "kaiser",
        ]
        | DefaultStr = DefaultStr(0),
        overlap: float | DefaultFloat = DefaultFloat(1.0),
        orientation: int | Literal["vertical", "horizontal"] | DefaultStr = DefaultStr("vertical"),
        **kwargs: Any,
    ) -> "AudioStream":
        """

        18.32 spectrumsynth
        Synthesize audio from 2 input video spectrums, first input stream represents
        magnitude across time and second represents phase across time.
        The filter will transform from frequency domain as displayed in videos back
        to time domain as presented in audio output.

        This filter is primarily created for reversing processed showspectrum
        filter outputs, but can synthesize sound from other spectrograms too.
        But in such case results are going to be poor if the phase data is not
        available, because in such cases phase data need to be recreated, usually
        it’s just recreated from random noise.
        For best results use gray only output (channel color mode in
        showspectrum filter) and log scale for magnitude video and
        lin scale for phase video. To produce phase, for 2nd video, use
        data option. Inputs videos should generally use fullframe
        slide mode as that saves resources needed for decoding video.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int sample_rate: Specify sample rate of output audio, the sample rate of audio from which spectrum was generated may differ.
        :param int channels: Set number of channels represented in input video spectrums.
        :param int scale: Set scale which was used when generating magnitude input spectrum. Can be lin or log. Default is log.
        :param int slide: Set slide which was used when generating inputs spectrums. Can be replace, scroll, fullframe or rscroll. Default is fullframe.
        :param int win_func: Set window function used for resynthesis.
        :param float overlap: Set window overlap. In range [0, 1]. Default is 1, which means optimal overlap for selected window function will be picked.
        :param int orientation: Set orientation of input videos. Can be vertical or horizontal. Default is vertical.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#spectrumsynth

        """
        filter_node = FilterNode(
            name="spectrumsynth",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.audio],
            inputs=[
                self,
                _phase,
            ],
            kwargs={
                "sample_rate": sample_rate,
                "channels": channels,
                "scale": scale,
                "slide": slide,
                "win_func": win_func,
                "overlap": overlap,
                "orientation": orientation,
            }
            | kwargs,
        )
        return filter_node.audio(0)

    def split(self, *, outputs: int | DefaultInt = DefaultInt(2), **kwargs: Any) -> FilterNode:
        """

        18.33 split, asplit
        Split input into several identical outputs.

        asplit works with audio input, split with video.

        The filter accepts a single parameter which specifies the number of outputs. If
        unspecified, it defaults to 2.

        Parameters:
        ----------

        :param int outputs: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#split_002c-asplit

        """
        filter_node = FilterNode(
            name="split",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video] * outputs,
            inputs=[
                self,
            ],
            kwargs={
                "outputs": outputs,
            }
            | kwargs,
        )

        return filter_node

    def spp(
        self,
        *,
        quality: int | DefaultInt = DefaultInt(3),
        qp: int | DefaultInt = DefaultInt(0),
        mode: int | Literal["hard", "soft"] | DefaultStr = DefaultStr("hard"),
        use_bframe_qp: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.241 spp
        Apply a simple postprocessing filter that compresses and decompresses the image
        at several (or - in the case of quality level 6 - all) shifts
        and average the results.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int quality: Set quality. This option defines the number of levels for averaging. It accepts an integer in the range 0-6. If set to 0, the filter will have no effect. A value of 6 means the higher quality. For each increment of that value the speed drops by a factor of approximately 2. Default value is 3.
        :param int qp: Force a constant quantization parameter. If not set, the filter will use the QP from the video stream (if available).
        :param int mode: Set thresholding mode. Available modes are: ‘hard’ Set hard thresholding (default). ‘soft’ Set soft thresholding (better de-ringing effect, but likely blurrier).
        :param bool use_bframe_qp: Enable the use of the QP from the B-Frames if set to 1. Using this option may cause flicker since the B-Frames have often larger QP. Default is 0 (not enabled).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#spp

        """
        filter_node = FilterNode(
            name="spp",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "quality": quality,
                "qp": qp,
                "mode": mode,
                "use_bframe_qp": use_bframe_qp,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def sr(
        self,
        *,
        dnn_backend: int | DefaultInt = DefaultInt(1),
        scale_factor: int | DefaultInt = DefaultInt(2),
        model: str,
        input: str | DefaultStr = DefaultStr("x"),
        output: str | DefaultStr = DefaultStr("y"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.242 sr
        Scale the input by applying one of the super-resolution methods based on
        convolutional neural networks. Supported models:


         Super-Resolution Convolutional Neural Network model (SRCNN).
        See https://arxiv.org/abs/1501.00092.

         Efficient Sub-Pixel Convolutional Neural Network model (ESPCN).
        See https://arxiv.org/abs/1609.05158.

        Training scripts as well as scripts for model file (.pb) saving can be found at
        https://github.com/XueweiMeng/sr/tree/sr_dnn_native. Original repository
        is at https://github.com/HighVoltageRocknRoll/sr.git.

        The filter accepts the following options:


        To get full functionality (such as async execution), please use the dnn_processing filter.

        Parameters:
        ----------

        :param int dnn_backend: Specify which DNN backend to use for model loading and execution. This option accepts the following values: ‘tensorflow’ TensorFlow backend. To enable this backend you need to install the TensorFlow for C library (see https://www.tensorflow.org/install/lang_c) and configure FFmpeg with --enable-libtensorflow
        :param int scale_factor: Set scale factor for SRCNN model. Allowed values are 2, 3 and 4. Default value is 2. Scale factor is necessary for SRCNN model, because it accepts input upscaled using bicubic upscaling with proper scale factor.
        :param str model: Set path to model file specifying network architecture and its parameters. Note that different backends use different file formats. TensorFlow, OpenVINO backend can load files for only its format.
        :param str input: None
        :param str output: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#sr

        """
        filter_node = FilterNode(
            name="sr",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dnn_backend": dnn_backend,
                "scale_factor": scale_factor,
                "model": model,
                "input": input,
                "output": output,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def ssim(self, _reference: "VideoStream", *, stats_file: str, **kwargs: Any) -> "VideoStream":
        """

        11.243 ssim
        Obtain the SSIM (Structural SImilarity Metric) between two input videos.

        This filter takes in input two input videos, the first input is
        considered the "main" source and is passed unchanged to the
        output. The second input is used as a "reference" video for computing
        the SSIM.

        Both video inputs must have the same resolution and pixel format for
        this filter to work correctly. Also it assumes that both inputs
        have the same number of frames, which are compared one by one.

        The filter stores the calculated SSIM of each frame.

        The description of the accepted parameters follows.


        The file printed if stats_file is selected, contains a sequence of
        key/value pairs of the form key:value for each compared
        couple of frames.

        A description of each shown parameter follows:


        This filter also supports the framesync options.

        Parameters:
        ----------

        :param str stats_file: If specified the filter will use the named file to save the SSIM of each individual frame. When filename equals "-" the data is sent to standard output.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#ssim

        """
        filter_node = FilterNode(
            name="ssim",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _reference,
            ],
            kwargs={
                "stats_file": stats_file,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def stereo3d(
        self,
        *,
        _in: int
        | Literal[
            "ab2l",
            "tb2l",
            "ab2r",
            "tb2r",
            "abl",
            "tbl",
            "abr",
            "tbr",
            "al",
            "ar",
            "sbs2l",
            "sbs2r",
            "sbsl",
            "sbsr",
            "irl",
            "irr",
            "icl",
            "icr",
        ]
        | DefaultStr = DefaultStr("sbsl"),
        out: int
        | Literal[
            "ab2l",
            "tb2l",
            "ab2r",
            "tb2r",
            "abl",
            "tbl",
            "abr",
            "tbr",
            "agmc",
            "agmd",
            "agmg",
            "agmh",
            "al",
            "ar",
            "arbg",
            "arcc",
            "arcd",
            "arcg",
            "arch",
            "argg",
            "aybc",
            "aybd",
            "aybg",
            "aybh",
            "irl",
            "irr",
            "ml",
            "mr",
            "sbs2l",
            "sbs2r",
            "sbsl",
            "sbsr",
            "chl",
            "chr",
            "icl",
            "icr",
            "hdmi",
        ]
        | DefaultStr = DefaultStr("arcd"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.244 stereo3d
        Convert between different stereoscopic image formats.

        The filters accept the following options:

        Parameters:
        ----------

        :param int _in: Set stereoscopic image format of input. Available values for input image formats are: ‘sbsl’ side by side parallel (left eye left, right eye right) ‘sbsr’ side by side crosseye (right eye left, left eye right) ‘sbs2l’ side by side parallel with half width resolution (left eye left, right eye right) ‘sbs2r’ side by side crosseye with half width resolution (right eye left, left eye right) ‘abl’ ‘tbl’ above-below (left eye above, right eye below) ‘abr’ ‘tbr’ above-below (right eye above, left eye below) ‘ab2l’ ‘tb2l’ above-below with half height resolution (left eye above, right eye below) ‘ab2r’ ‘tb2r’ above-below with half height resolution (right eye above, left eye below) ‘al’ alternating frames (left eye first, right eye second) ‘ar’ alternating frames (right eye first, left eye second) ‘irl’ interleaved rows (left eye has top row, right eye starts on next row) ‘irr’ interleaved rows (right eye has top row, left eye starts on next row) ‘icl’ interleaved columns, left eye first ‘icr’ interleaved columns, right eye first Default value is ‘sbsl’.
        :param int out: Set stereoscopic image format of output. ‘sbsl’ side by side parallel (left eye left, right eye right) ‘sbsr’ side by side crosseye (right eye left, left eye right) ‘sbs2l’ side by side parallel with half width resolution (left eye left, right eye right) ‘sbs2r’ side by side crosseye with half width resolution (right eye left, left eye right) ‘abl’ ‘tbl’ above-below (left eye above, right eye below) ‘abr’ ‘tbr’ above-below (right eye above, left eye below) ‘ab2l’ ‘tb2l’ above-below with half height resolution (left eye above, right eye below) ‘ab2r’ ‘tb2r’ above-below with half height resolution (right eye above, left eye below) ‘al’ alternating frames (left eye first, right eye second) ‘ar’ alternating frames (right eye first, left eye second) ‘irl’ interleaved rows (left eye has top row, right eye starts on next row) ‘irr’ interleaved rows (right eye has top row, left eye starts on next row) ‘arbg’ anaglyph red/blue gray (red filter on left eye, blue filter on right eye) ‘argg’ anaglyph red/green gray (red filter on left eye, green filter on right eye) ‘arcg’ anaglyph red/cyan gray (red filter on left eye, cyan filter on right eye) ‘arch’ anaglyph red/cyan half colored (red filter on left eye, cyan filter on right eye) ‘arcc’ anaglyph red/cyan color (red filter on left eye, cyan filter on right eye) ‘arcd’ anaglyph red/cyan color optimized with the least squares projection of dubois (red filter on left eye, cyan filter on right eye) ‘agmg’ anaglyph green/magenta gray (green filter on left eye, magenta filter on right eye) ‘agmh’ anaglyph green/magenta half colored (green filter on left eye, magenta filter on right eye) ‘agmc’ anaglyph green/magenta colored (green filter on left eye, magenta filter on right eye) ‘agmd’ anaglyph green/magenta color optimized with the least squares projection of dubois (green filter on left eye, magenta filter on right eye) ‘aybg’ anaglyph yellow/blue gray (yellow filter on left eye, blue filter on right eye) ‘aybh’ anaglyph yellow/blue half colored (yellow filter on left eye, blue filter on right eye) ‘aybc’ anaglyph yellow/blue colored (yellow filter on left eye, blue filter on right eye) ‘aybd’ anaglyph yellow/blue color optimized with the least squares projection of dubois (yellow filter on left eye, blue filter on right eye) ‘ml’ mono output (left eye only) ‘mr’ mono output (right eye only) ‘chl’ checkerboard, left eye first ‘chr’ checkerboard, right eye first ‘icl’ interleaved columns, left eye first ‘icr’ interleaved columns, right eye first ‘hdmi’ HDMI frame pack Default value is ‘arcd’.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#stereo3d

        """
        filter_node = FilterNode(
            name="stereo3d",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "in": _in,
                "out": out,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def subtitles(
        self,
        *,
        filename: str,
        original_size: str,
        fontsdir: str,
        alpha: bool | DefaultInt = DefaultInt(0),
        charenc: str,
        stream_index: int | DefaultInt = DefaultInt(-1),
        force_style: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.246 subtitles
        Draw subtitles on top of input video using the libass library.

        To enable compilation of this filter you need to configure FFmpeg with
        --enable-libass. This filter also requires a build with libavcodec and
        libavformat to convert the passed subtitles file to ASS (Advanced Substation
        Alpha) subtitles format.

        The filter accepts the following options:


        If the first key is not specified, it is assumed that the first value
        specifies the filename.

        For example, to render the file sub.srt on top of the input
        video, use the command:

        subtitles=sub.srt

        which is equivalent to:

        subtitles=filename=sub.srt

        To render the default subtitles stream from file video.mkv, use:

        subtitles=video.mkv

        To render the second subtitles stream from that file, use:

        subtitles=video.mkv:si=1

        To make the subtitles stream from sub.srt appear in 80% transparent blue
        DejaVu Serif, use:

        subtitles=sub.srt:force_style='Fontname=DejaVu Serif,PrimaryColour=&HCCFF0000'

        Parameters:
        ----------

        :param str filename: Set the filename of the subtitle file to read. It must be specified.
        :param str original_size: Specify the size of the original video, the video for which the ASS file was composed. For the syntax of this option, check the (ffmpeg-utils)"Video size" section in the ffmpeg-utils manual. Due to a misdesign in ASS aspect ratio arithmetic, this is necessary to correctly scale the fonts if the aspect ratio has been changed.
        :param str fontsdir: Set a directory path containing fonts that can be used by the filter. These fonts will be used in addition to whatever the font provider uses.
        :param bool alpha: Process alpha channel, by default alpha channel is untouched.
        :param str charenc: Set subtitles input character encoding. subtitles filter only. Only useful if not UTF-8.
        :param int stream_index: Set subtitles stream index. subtitles filter only.
        :param str force_style: Override default style or script info parameters of the subtitles. It accepts a string containing ASS style format KEY=VALUE couples separated by ",".

        Ref: https://ffmpeg.org/ffmpeg-filters.html#subtitles

        """
        filter_node = FilterNode(
            name="subtitles",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "filename": filename,
                "original_size": original_size,
                "fontsdir": fontsdir,
                "alpha": alpha,
                "charenc": charenc,
                "stream_index": stream_index,
                "force_style": force_style,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def super2xsai(self, **kwargs: Any) -> "VideoStream":
        """

        11.247 super2xsai
        Scale the input by 2x and smooth using the Super2xSaI (Scale and
        Interpolate) pixel art scaling algorithm.

        Useful for enlarging pixel art images without reducing sharpness.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#super2xsai

        """
        filter_node = FilterNode(
            name="super2xsai",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def swaprect(
        self,
        *,
        w: str | DefaultStr = DefaultStr("w/2"),
        h: str | DefaultStr = DefaultStr("h/2"),
        x1: str | DefaultStr = DefaultStr("w/2"),
        y1: str | DefaultStr = DefaultStr("h/2"),
        x2: str | DefaultStr = DefaultStr("0"),
        y2: str | DefaultStr = DefaultStr("0"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.248 swaprect
        Swap two rectangular objects in video.

        This filter accepts the following options:


        The all options are expressions containing the following constants:

        Parameters:
        ----------

        :param str w: Set object width.
        :param str h: Set object height.
        :param str x1: Set 1st rect x coordinate.
        :param str y1: Set 1st rect y coordinate.
        :param str x2: Set 2nd rect x coordinate.
        :param str y2: Set 2nd rect y coordinate. All expressions are evaluated once for each frame.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#swaprect

        """
        filter_node = FilterNode(
            name="swaprect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "w": w,
                "h": h,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def swapuv(self, **kwargs: Any) -> "VideoStream":
        """

        11.249 swapuv
        Swap U & V plane.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#swapuv

        """
        filter_node = FilterNode(
            name="swapuv",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def tblend(
        self,
        *,
        c0_mode: int
        | Literal[
            "addition",
            "addition128",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "difference128",
            "grainextract",
            "divide",
            "dodge",
            "exclusion",
            "extremity",
            "freeze",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor",
            "softdifference",
            "geometric",
            "harmonic",
            "bleach",
            "stain",
            "interpolate",
            "hardoverlay",
        ]
        | DefaultStr = DefaultStr(0),
        c1_mode: int
        | Literal[
            "addition",
            "addition128",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "difference128",
            "grainextract",
            "divide",
            "dodge",
            "exclusion",
            "extremity",
            "freeze",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor",
            "softdifference",
            "geometric",
            "harmonic",
            "bleach",
            "stain",
            "interpolate",
            "hardoverlay",
        ]
        | DefaultStr = DefaultStr(0),
        c2_mode: int
        | Literal[
            "addition",
            "addition128",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "difference128",
            "grainextract",
            "divide",
            "dodge",
            "exclusion",
            "extremity",
            "freeze",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor",
            "softdifference",
            "geometric",
            "harmonic",
            "bleach",
            "stain",
            "interpolate",
            "hardoverlay",
        ]
        | DefaultStr = DefaultStr(0),
        c3_mode: int
        | Literal[
            "addition",
            "addition128",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "difference128",
            "grainextract",
            "divide",
            "dodge",
            "exclusion",
            "extremity",
            "freeze",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor",
            "softdifference",
            "geometric",
            "harmonic",
            "bleach",
            "stain",
            "interpolate",
            "hardoverlay",
        ]
        | DefaultStr = DefaultStr(0),
        all_mode: int
        | Literal[
            "addition",
            "addition128",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "difference128",
            "grainextract",
            "divide",
            "dodge",
            "exclusion",
            "extremity",
            "freeze",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor",
            "softdifference",
            "geometric",
            "harmonic",
            "bleach",
            "stain",
            "interpolate",
            "hardoverlay",
        ]
        | DefaultStr = DefaultStr(-1),
        c0_expr: str,
        c1_expr: str,
        c2_expr: str,
        c3_expr: str,
        all_expr: str,
        c0_opacity: float | DefaultFloat = DefaultFloat(1.0),
        c1_opacity: float | DefaultFloat = DefaultFloat(1.0),
        c2_opacity: float | DefaultFloat = DefaultFloat(1.0),
        c3_opacity: float | DefaultFloat = DefaultFloat(1.0),
        all_opacity: float | DefaultFloat = DefaultFloat(1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.250 tblend
        Blend successive video frames.

        See blend

        Parameters:
        ----------

        :param int c0_mode: None
        :param int c1_mode: None
        :param int c2_mode: None
        :param int c3_mode: None
        :param int all_mode: None
        :param str c0_expr: None
        :param str c1_expr: None
        :param str c2_expr: None
        :param str c3_expr: None
        :param str all_expr: None
        :param float c0_opacity: None
        :param float c1_opacity: None
        :param float c2_opacity: None
        :param float c3_opacity: None
        :param float all_opacity: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tblend

        """
        filter_node = FilterNode(
            name="tblend",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "c0_mode": c0_mode,
                "c1_mode": c1_mode,
                "c2_mode": c2_mode,
                "c3_mode": c3_mode,
                "all_mode": all_mode,
                "c0_expr": c0_expr,
                "c1_expr": c1_expr,
                "c2_expr": c2_expr,
                "c3_expr": c3_expr,
                "all_expr": all_expr,
                "c0_opacity": c0_opacity,
                "c1_opacity": c1_opacity,
                "c2_opacity": c2_opacity,
                "c3_opacity": c3_opacity,
                "all_opacity": all_opacity,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def telecine(
        self,
        *,
        first_field: int | Literal["top", "t", "bottom", "b"] | DefaultStr = DefaultStr("top"),
        pattern: str | DefaultStr = DefaultStr("23"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.251 telecine
        Apply telecine process to the video.

        This filter accepts the following options:



        Some typical patterns:

        NTSC output (30i):
        27.5p: 32222
        24p: 23 (classic)
        24p: 2332 (preferred)
        20p: 33
        18p: 334
        16p: 3444

        PAL output (25i):
        27.5p: 12222
        24p: 222222222223 ("Euro pulldown")
        16.67p: 33
        16p: 33333334

        Parameters:
        ----------

        :param int first_field: ‘top, t’ top field first ‘bottom, b’ bottom field first The default value is top.
        :param str pattern: A string of numbers representing the pulldown pattern you wish to apply. The default value is 23.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#telecine

        """
        filter_node = FilterNode(
            name="telecine",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "first_field": first_field,
                "pattern": pattern,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def thistogram(
        self,
        *,
        width: int | DefaultInt = DefaultInt(0),
        display_mode: int | Literal["overlay", "parade", "stack"] | DefaultStr = DefaultStr("stack"),
        levels_mode: int | Literal["linear", "logarithmic"] | DefaultStr = DefaultStr("linear"),
        components: int | DefaultInt = DefaultInt(7),
        bgopacity: float | DefaultFloat = DefaultFloat(0.9),
        envelope: bool | DefaultInt = DefaultInt(0),
        ecolor: str | DefaultStr = DefaultStr("gold"),
        slide: int | Literal["frame", "replace", "scroll", "rscroll", "picture"] | DefaultStr = DefaultStr("replace"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.252 thistogram
        Compute and draw a color distribution histogram for the input video across time.

        Unlike histogram video filter which only shows histogram of single input frame
        at certain time, this filter shows also past histograms of number of frames defined
        by width option.

        The computed histogram is a representation of the color component
        distribution in an image.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int width: Set width of single color component output. Default value is 0. Value of 0 means width will be picked from input video. This also set number of passed histograms to keep. Allowed range is [0, 8192].
        :param int display_mode: Set display mode. It accepts the following values: ‘stack’ Per color component graphs are placed below each other. ‘parade’ Per color component graphs are placed side by side. ‘overlay’ Presents information identical to that in the parade, except that the graphs representing color components are superimposed directly over one another. Default is stack.
        :param int levels_mode: Set mode. Can be either linear, or logarithmic. Default is linear.
        :param int components: Set what color components to display. Default is 7.
        :param float bgopacity: Set background opacity. Default is 0.9.
        :param bool envelope: Show envelope. Default is disabled.
        :param str ecolor: Set envelope color. Default is gold.
        :param int slide: Set slide mode. Available values for slide is: ‘frame’ Draw new frame when right border is reached. ‘replace’ Replace old columns with new ones. ‘scroll’ Scroll from right to left. ‘rscroll’ Scroll from left to right. ‘picture’ Draw single picture. Default is replace.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#thistogram

        """
        filter_node = FilterNode(
            name="thistogram",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "width": width,
                "display_mode": display_mode,
                "levels_mode": levels_mode,
                "components": components,
                "bgopacity": bgopacity,
                "envelope": envelope,
                "ecolor": ecolor,
                "slide": slide,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def threshold(
        self,
        _threshold: "VideoStream",
        _min: "VideoStream",
        _max: "VideoStream",
        *,
        planes: int | DefaultInt = DefaultInt(15),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.253 threshold
        Apply threshold effect to video stream.

        This filter needs four video streams to perform thresholding.
        First stream is stream we are filtering.
        Second stream is holding threshold values, third stream is holding min values,
        and last, fourth stream is holding max values.

        The filter accepts the following option:


        For example if first stream pixel’s component value is less then threshold value
        of pixel component from 2nd threshold stream, third stream value will picked,
        otherwise fourth stream pixel component value will be picked.

        Using color source filter one can perform various types of thresholding:

        Parameters:
        ----------

        :param int planes: Set which planes will be processed, unprocessed planes will be copied. By default value 0xf, all planes will be processed.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#threshold

        """
        filter_node = FilterNode(
            name="threshold",
            input_typings=[StreamType.video, StreamType.video, StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _threshold,
                _min,
                _max,
            ],
            kwargs={
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def thumbnail(
        self,
        *,
        n: int | DefaultInt = DefaultInt(100),
        log: int | Literal["quiet", "info", "verbose"] | DefaultStr = DefaultStr("info"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.254 thumbnail
        Select the most representative frame in a given sequence of consecutive frames.

        The filter accepts the following options:


        Since the filter keeps track of the whole frames sequence, a bigger n
        value will result in a higher memory usage, so a high value is not recommended.

        Parameters:
        ----------

        :param int n: Set the frames batch size to analyze; in a set of n frames, the filter will pick one of them, and then handle the next batch of n frames until the end. Default is 100.
        :param int log: Set the log level to display picked frame stats. Default is info.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#thumbnail

        """
        filter_node = FilterNode(
            name="thumbnail",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "n": n,
                "log": log,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tile(
        self,
        *,
        layout: str | DefaultStr = DefaultStr("6x5"),
        nb_frames: int | DefaultInt = DefaultInt(0),
        margin: int | DefaultInt = DefaultInt(0),
        padding: int | DefaultInt = DefaultInt(0),
        color: str | DefaultStr = DefaultStr("black"),
        overlap: int | DefaultInt = DefaultInt(0),
        init_padding: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.255 tile
        Tile several successive frames together.

        The untile filter can do the reverse.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str layout: Set the grid size in the form COLUMNSxROWS. Range is up to UINT_MAX cells. Default is 6x5.
        :param int nb_frames: Set the maximum number of frames to render in the given area. It must be less than or equal to wxh. The default value is 0, meaning all the area will be used.
        :param int margin: Set the outer border margin in pixels. Range is 0 to 1024. Default is 0.
        :param int padding: Set the inner border thickness (i.e. the number of pixels between frames). For more advanced padding options (such as having different values for the edges), refer to the pad video filter. Range is 0 to 1024. Default is 0.
        :param str color: Specify the color of the unused area. For the syntax of this option, check the (ffmpeg-utils)"Color" section in the ffmpeg-utils manual. The default value of color is "black".
        :param int overlap: Set the number of frames to overlap when tiling several successive frames together. The value must be between 0 and nb_frames - 1. Default is 0.
        :param int init_padding: Set the number of frames to initially be empty before displaying first output frame. This controls how soon will one get first output frame. The value must be between 0 and nb_frames - 1. Default is 0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tile

        """
        filter_node = FilterNode(
            name="tile",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "layout": layout,
                "nb_frames": nb_frames,
                "margin": margin,
                "padding": padding,
                "color": color,
                "overlap": overlap,
                "init_padding": init_padding,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tiltandshift(
        self,
        *,
        tilt: int | DefaultInt = DefaultInt(1),
        start: int | Literal["none", "frame", "black"] | DefaultStr = DefaultStr("none"),
        end: int | Literal["none", "frame", "black"] | DefaultStr = DefaultStr("none"),
        hold: int | DefaultInt = DefaultInt(0),
        pad: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.256 tiltandshift
        What happens when you invert time and space?

        Normally a video is composed of several frames that represent a different
        instant of time and shows a scence that evolves in the space captured by the
        frame. This filter is the antipode of that concept, taking inspiration by
        tilt and shift photography.

        A filtered frame contains the whole timeline of events composing the sequence,
        and this is obtained by placing a slice of pixels from each frame into a single
        one. However, since there are no infinite-width frames, this is done up the
        width of the input frame, and a video is recomposed by shifting away one
        column for each subsequent frame. In order to map space to time, the filter
        tilts each input frame as well, so that motion is preseved. This is accomplished
        by progressively selecting a different column from each input frame.

        The end result is a sort of inverted parralax, so that far away objects move
        much faster that the ones in the front. The ideal conditions for this video
        effect are when there is either very little motion and the backgroud is static,
        or when there is a lot of motion and a very wide depth of field (eg. wide
        panorama, while moving on a train).

        The filter accepts the following parameters:


        Normally the filter shifts and tils from the very first frame, and stops when
        the last one is received. However, before filtering starts, normal video may
        be preseved, so that the effect is slowly shifted in its place. Similarly,
        the last video frame may be reconstructed at the end. Alternatively it is
        possible to just start and end with black.

        Parameters:
        ----------

        :param int tilt: Tilt video while shifting (default). When unset, video will be sliding a static image, composed of the first column of each frame.
        :param int start: What to do at the start of filtering (see below).
        :param int end: What to do at the end of filtering (see below).
        :param int hold: How many columns should pass through before start of filtering.
        :param int pad: How many columns should be inserted before end of filtering.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tiltandshift

        """
        filter_node = FilterNode(
            name="tiltandshift",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "tilt": tilt,
                "start": start,
                "end": end,
                "hold": hold,
                "pad": pad,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tinterlace(
        self,
        *,
        mode: int
        | Literal[
            "merge", "drop_even", "drop_odd", "pad", "interleave_top", "interleave_bottom", "interlacex2", "mergex2"
        ]
        | DefaultStr = DefaultStr("merge"),
        flags: str
        | Literal["low_pass_filter", "vlpf", "complex_filter", "cvlpf", "exact_tb", "bypass_il"]
        | DefaultStr = DefaultStr(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.257 tinterlace
        Perform various types of temporal field interlacing.

        Frames are counted starting from 1, so the first input frame is
        considered odd.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int mode: Specify the mode of the interlacing. This option can also be specified as a value alone. See below for a list of values for this option. Available values are: ‘merge, 0’ Move odd frames into the upper field, even into the lower field, generating a double height frame at half frame rate. ------> time Input: Frame 1 Frame 2 Frame 3 Frame 4 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 Output: 11111 33333 22222 44444 11111 33333 22222 44444 11111 33333 22222 44444 11111 33333 22222 44444 ‘drop_even, 1’ Only output odd frames, even frames are dropped, generating a frame with unchanged height at half frame rate. ------> time Input: Frame 1 Frame 2 Frame 3 Frame 4 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 Output: 11111 33333 11111 33333 11111 33333 11111 33333 ‘drop_odd, 2’ Only output even frames, odd frames are dropped, generating a frame with unchanged height at half frame rate. ------> time Input: Frame 1 Frame 2 Frame 3 Frame 4 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 Output: 22222 44444 22222 44444 22222 44444 22222 44444 ‘pad, 3’ Expand each frame to full height, but pad alternate lines with black, generating a frame with double height at the same input frame rate. ------> time Input: Frame 1 Frame 2 Frame 3 Frame 4 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 Output: 11111 ..... 33333 ..... ..... 22222 ..... 44444 11111 ..... 33333 ..... ..... 22222 ..... 44444 11111 ..... 33333 ..... ..... 22222 ..... 44444 11111 ..... 33333 ..... ..... 22222 ..... 44444 ‘interleave_top, 4’ Interleave the upper field from odd frames with the lower field from even frames, generating a frame with unchanged height at half frame rate. ------> time Input: Frame 1 Frame 2 Frame 3 Frame 4 11111<- 22222 33333<- 44444 11111 22222<- 33333 44444<- 11111<- 22222 33333<- 44444 11111 22222<- 33333 44444<- Output: 11111 33333 22222 44444 11111 33333 22222 44444 ‘interleave_bottom, 5’ Interleave the lower field from odd frames with the upper field from even frames, generating a frame with unchanged height at half frame rate. ------> time Input: Frame 1 Frame 2 Frame 3 Frame 4 11111 22222<- 33333 44444<- 11111<- 22222 33333<- 44444 11111 22222<- 33333 44444<- 11111<- 22222 33333<- 44444 Output: 22222 44444 11111 33333 22222 44444 11111 33333 ‘interlacex2, 6’ Double frame rate with unchanged height. Frames are inserted each containing the second temporal field from the previous input frame and the first temporal field from the next input frame. This mode relies on the top_field_first flag. Useful for interlaced video displays with no field synchronisation. ------> time Input: Frame 1 Frame 2 Frame 3 Frame 4 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 Output: 11111 22222 22222 33333 33333 44444 44444 11111 11111 22222 22222 33333 33333 44444 11111 22222 22222 33333 33333 44444 44444 11111 11111 22222 22222 33333 33333 44444 ‘mergex2, 7’ Move odd frames into the upper field, even into the lower field, generating a double height frame at same frame rate. ------> time Input: Frame 1 Frame 2 Frame 3 Frame 4 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 11111 22222 33333 44444 Output: 11111 33333 33333 55555 22222 22222 44444 44444 11111 33333 33333 55555 22222 22222 44444 44444 11111 33333 33333 55555 22222 22222 44444 44444 11111 33333 33333 55555 22222 22222 44444 44444 Numeric values are deprecated but are accepted for backward compatibility reasons. Default mode is merge.
        :param str flags: Specify flags influencing the filter process. Available value for flags is: low_pass_filter, vlpf Enable linear vertical low-pass filtering in the filter. Vertical low-pass filtering is required when creating an interlaced destination from a progressive source which contains high-frequency vertical detail. Filtering will reduce interlace ’twitter’ and Moire patterning. complex_filter, cvlpf Enable complex vertical low-pass filtering. This will slightly less reduce interlace ’twitter’ and Moire patterning but better retain detail and subjective sharpness impression. bypass_il Bypass already interlaced frames, only adjust the frame rate. Vertical low-pass filtering and bypassing already interlaced frames can only be enabled for mode interleave_top and interleave_bottom.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tinterlace

        """
        filter_node = FilterNode(
            name="tinterlace",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "flags": flags,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tlut2(
        self,
        *,
        c0: str | DefaultStr = DefaultStr("x"),
        c1: str | DefaultStr = DefaultStr("x"),
        c2: str | DefaultStr = DefaultStr("x"),
        c3: str | DefaultStr = DefaultStr("x"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.154 lut2, tlut2
        The lut2 filter takes two input streams and outputs one
        stream.

        The tlut2 (time lut2) filter takes two consecutive frames
        from one single stream.

        This filter accepts the following parameters:

        The lut2 filter also supports the framesync options.

        Each of them specifies the expression to use for computing the lookup table for
        the corresponding pixel component values.

        The exact component associated to each of the c* options depends on the
        format in inputs.

        The expressions can contain the following constants:


        All expressions default to "x".

        Parameters:
        ----------

        :param str c0: set first pixel component expression
        :param str c1: set second pixel component expression
        :param str c2: set third pixel component expression
        :param str c3: set fourth pixel component expression, corresponds to the alpha component

        Ref: https://ffmpeg.org/ffmpeg-filters.html#lut2_002c-tlut2

        """
        filter_node = FilterNode(
            name="tlut2",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "c0": c0,
                "c1": c1,
                "c2": c2,
                "c3": c3,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tmedian(
        self,
        *,
        radius: int | DefaultInt = DefaultInt(1),
        planes: int | DefaultInt = DefaultInt(15),
        percentile: float | DefaultFloat = DefaultFloat(0.5),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.258 tmedian
        Pick median pixels from several successive input video frames.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int radius: Set radius of median filter. Default is 1. Allowed range is from 1 to 127.
        :param int planes: Set which planes to filter. Default value is 15, by which all planes are processed.
        :param float percentile: Set median percentile. Default value is 0.5. Default value of 0.5 will pick always median values, while 0 will pick minimum values, and 1 maximum values.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tmedian

        """
        filter_node = FilterNode(
            name="tmedian",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "radius": radius,
                "planes": planes,
                "percentile": percentile,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tmidequalizer(
        self,
        *,
        radius: int | DefaultInt = DefaultInt(5),
        sigma: float | DefaultFloat = DefaultFloat(0.5),
        planes: int | DefaultStr = DefaultStr("0xF"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.259 tmidequalizer
        Apply Temporal Midway Video Equalization effect.

        Midway Video Equalization adjusts a sequence of video frames to have the same
        histograms, while maintaining their dynamics as much as possible. It’s
        useful for e.g. matching exposures from a video frames sequence.

        This filter accepts the following option:

        Parameters:
        ----------

        :param int radius: Set filtering radius. Default is 5. Allowed range is from 1 to 127.
        :param float sigma: Set filtering sigma. Default is 0.5. This controls strength of filtering. Setting this option to 0 effectively does nothing.
        :param int planes: Set which planes to process. Default is 15, which is all available planes.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tmidequalizer

        """
        filter_node = FilterNode(
            name="tmidequalizer",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "radius": radius,
                "sigma": sigma,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tmix(
        self,
        *,
        frames: int | DefaultInt = DefaultInt(3),
        weights: str | DefaultStr = DefaultStr("1 1 1"),
        scale: float | DefaultFloat = DefaultFloat(0.0),
        planes: str | DefaultStr = DefaultStr(15),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.260 tmix
        Mix successive video frames.

        A description of the accepted options follows.

        Parameters:
        ----------

        :param int frames: The number of successive frames to mix. If unspecified, it defaults to 3.
        :param str weights: Specify weight of each input video frame. Each weight is separated by space. If number of weights is smaller than number of frames last specified weight will be used for all remaining unset weights.
        :param float scale: Specify scale, if it is set it will be multiplied with sum of each weight multiplied with pixel values to give final destination pixel value. By default scale is auto scaled to sum of weights.
        :param str planes: Set which planes to filter. Default is all. Allowed range is from 0 to 15.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tmix

        """
        filter_node = FilterNode(
            name="tmix",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "frames": frames,
                "weights": weights,
                "scale": scale,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tonemap(
        self,
        *,
        tonemap: int
        | Literal["none", "linear", "gamma", "clip", "reinhard", "hable", "mobius"]
        | DefaultStr = DefaultStr("none"),
        param: float | DefaultStr = DefaultStr('__builtin_nanf("0x7fc00000")'),
        desat: float | DefaultFloat = DefaultFloat(2.0),
        peak: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.261 tonemap
        Tone map colors from different dynamic ranges.

        This filter expects data in single precision floating point, as it needs to
        operate on (and can output) out-of-range values. Another filter, such as
        zscale, is needed to convert the resulting frame to a usable format.

        The tonemapping algorithms implemented only work on linear light, so input
        data should be linearized beforehand (and possibly correctly tagged).


        ffmpeg -i INPUT -vf zscale=transfer=linear,tonemap=clip,zscale=transfer=bt709,format=yuv420p OUTPUT

        Parameters:
        ----------

        :param int tonemap: None
        :param float param: None
        :param float desat: None
        :param float peak: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tonemap

        """
        filter_node = FilterNode(
            name="tonemap",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "tonemap": tonemap,
                "param": param,
                "desat": desat,
                "peak": peak,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tonemap_opencl(
        self,
        *,
        tonemap: int
        | Literal["none", "linear", "gamma", "clip", "reinhard", "hable", "mobius"]
        | DefaultStr = DefaultStr("none"),
        transfer: int | Literal["bt709", "bt2020"] | DefaultStr = DefaultStr("bt709"),
        matrix: int | Literal["bt709", "bt2020"] | DefaultStr = DefaultStr(-1),
        primaries: int | Literal["bt709", "bt2020"] | DefaultStr = DefaultStr(-1),
        range: int | Literal["tv", "pc", "limited", "full"] | DefaultStr = DefaultStr(-1),
        format: str | DefaultStr = DefaultStr("AV_PIX_FMT_NONE"),
        peak: float | DefaultFloat = DefaultFloat(0.0),
        param: float | DefaultStr = DefaultStr('__builtin_nanf("0x7fc00000")'),
        desat: float | DefaultFloat = DefaultFloat(0.5),
        threshold: float | DefaultFloat = DefaultFloat(0.2),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.16 tonemap_opencl
        Perform HDR(PQ/HLG) to SDR conversion with tone-mapping.

        It accepts the following parameters:

        Parameters:
        ----------

        :param int tonemap: Specify the tone-mapping operator to be used. Same as tonemap option in tonemap.
        :param int transfer: Set the output transfer characteristics. Possible values are: bt709 bt2020 Default is bt709.
        :param int matrix: Set the output colorspace matrix. Possible value are: bt709 bt2020 Default is same as input.
        :param int primaries: Set the output color primaries. Possible values are: bt709 bt2020 Default is same as input.
        :param int range: Set the output color range. Possible values are: tv/mpeg pc/jpeg Default is same as input.
        :param str format: Specify the output pixel format. Currently supported formats are: p010 nv12
        :param float peak: None
        :param float param: Tune the tone mapping algorithm. same as param option in tonemap.
        :param float desat: Apply desaturation for highlights that exceed this level of brightness. The higher the parameter, the more color information will be preserved. This setting helps prevent unnaturally blown-out colors for super-highlights, by (smoothly) turning into white instead. This makes images feel more natural, at the cost of reducing information about out-of-range colors. The default value is 0.5, and the algorithm here is a little different from the cpu version tonemap currently. A setting of 0.0 disables this option.
        :param float threshold: The tonemapping algorithm parameters is fine-tuned per each scene. And a threshold is used to detect whether the scene has changed or not. If the distance between the current frame average brightness and the current running average exceeds a threshold value, we would re-calculate scene average and peak brightness. The default value is 0.2.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tonemap_005fopencl

        """
        filter_node = FilterNode(
            name="tonemap_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "tonemap": tonemap,
                "transfer": transfer,
                "matrix": matrix,
                "primaries": primaries,
                "range": range,
                "format": format,
                "peak": peak,
                "param": param,
                "desat": desat,
                "threshold": threshold,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tonemap_vaapi(self, *, format: str, matrix: str, primaries: str, transfer: str, **kwargs: Any) -> "VideoStream":
        """

        13.2 tonemap_vaapi
        Perform HDR(High Dynamic Range) to SDR(Standard Dynamic Range) conversion with tone-mapping.
        It maps the dynamic range of HDR10 content to the SDR content.
        It currently only accepts HDR10 as input.

        It accepts the following parameters:

        Parameters:
        ----------

        :param str format: Specify the output pixel format. Currently supported formats are: p010 nv12 Default is nv12.
        :param str matrix: Set the output colorspace matrix. Default is same as input.
        :param str primaries: Set the output color primaries. Default is same as input.
        :param str transfer: Set the output transfer characteristics. Default is bt709.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tonemap_005fvaapi

        """
        filter_node = FilterNode(
            name="tonemap_vaapi",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "format": format,
                "matrix": matrix,
                "primaries": primaries,
                "transfer": transfer,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def tpad(
        self,
        *,
        start: int | DefaultInt = DefaultInt(0),
        stop: int | DefaultInt = DefaultInt(0),
        start_mode: int | Literal["add", "clone"] | DefaultStr = DefaultStr("add"),
        stop_mode: int | Literal["add", "clone"] | DefaultStr = DefaultStr("add"),
        start_duration: int | DefaultInt = DefaultInt(0),
        stop_duration: int | DefaultInt = DefaultInt(0),
        color: str | DefaultStr = DefaultStr("black"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.262 tpad
        Temporarily pad video frames.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int start: Specify number of delay frames before input video stream. Default is 0.
        :param int stop: Specify number of padding frames after input video stream. Set to -1 to pad indefinitely. Default is 0.
        :param int start_mode: Set kind of frames added to beginning of stream. Can be either add or clone. With add frames of solid-color are added. With clone frames are clones of first frame. Default is add.
        :param int stop_mode: Set kind of frames added to end of stream. Can be either add or clone. With add frames of solid-color are added. With clone frames are clones of last frame. Default is add.
        :param int start_duration: Specify the duration of the start/stop delay. See (ffmpeg-utils)the Time duration section in the ffmpeg-utils(1) manual for the accepted syntax. These options override start and stop. Default is 0.
        :param int stop_duration: Specify the duration of the start/stop delay. See (ffmpeg-utils)the Time duration section in the ffmpeg-utils(1) manual for the accepted syntax. These options override start and stop. Default is 0.
        :param str color: Specify the color of the padded area. For the syntax of this option, check the (ffmpeg-utils)"Color" section in the ffmpeg-utils manual. The default value of color is "black".

        Ref: https://ffmpeg.org/ffmpeg-filters.html#tpad

        """
        filter_node = FilterNode(
            name="tpad",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "start": start,
                "stop": stop,
                "start_mode": start_mode,
                "stop_mode": stop_mode,
                "start_duration": start_duration,
                "stop_duration": stop_duration,
                "color": color,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def transpose(
        self,
        *,
        dir: int | DefaultStr = DefaultStr("TRANSPOSE_CCLOCK_FLIP"),
        passthrough: int | Literal["none", "portrait", "landscape"] | DefaultStr = DefaultStr("none"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.263 transpose
        Transpose rows with columns in the input video and optionally flip it.

        It accepts the following parameters:


        For example to rotate by 90 degrees clockwise and preserve portrait
        layout:

        transpose=dir=1:passthrough=portrait

        The command above can also be specified as:

        transpose=1:portrait

        Parameters:
        ----------

        :param int dir: Specify the transposition direction. Can assume the following values: ‘0, 4, cclock_flip’ Rotate by 90 degrees counterclockwise and vertically flip (default), that is: L.R L.l . . -> . . l.r R.r ‘1, 5, clock’ Rotate by 90 degrees clockwise, that is: L.R l.L . . -> . . l.r r.R ‘2, 6, cclock’ Rotate by 90 degrees counterclockwise, that is: L.R R.r . . -> . . l.r L.l ‘3, 7, clock_flip’ Rotate by 90 degrees clockwise and vertically flip, that is: L.R r.R . . -> . . l.r l.L For values between 4-7, the transposition is only done if the input video geometry is portrait and not landscape. These values are deprecated, the passthrough option should be used instead. Numerical values are deprecated, and should be dropped in favor of symbolic constants.
        :param int passthrough: Do not apply the transposition if the input geometry matches the one specified by the specified value. It accepts the following values: ‘none’ Always apply transposition. ‘portrait’ Preserve portrait geometry (when height >= width). ‘landscape’ Preserve landscape geometry (when width >= height). Default value is none.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#transpose

        """
        filter_node = FilterNode(
            name="transpose",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dir": dir,
                "passthrough": passthrough,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def transpose_npp(
        self,
        *,
        dir: int | Literal["cclock_flip", "clock", "cclock", "clock_flip"] | DefaultStr = DefaultStr("cclock_flip"),
        passthrough: int | Literal["none", "landscape", "portrait"] | DefaultStr = DefaultStr("none"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.264 transpose_npp
        Transpose rows with columns in the input video and optionally flip it.
        For more in depth examples see the transpose video filter, which shares mostly the same options.

        It accepts the following parameters:

        Parameters:
        ----------

        :param int dir: Specify the transposition direction. Can assume the following values: ‘cclock_flip’ Rotate by 90 degrees counterclockwise and vertically flip. (default) ‘clock’ Rotate by 90 degrees clockwise. ‘cclock’ Rotate by 90 degrees counterclockwise. ‘clock_flip’ Rotate by 90 degrees clockwise and vertically flip.
        :param int passthrough: Do not apply the transposition if the input geometry matches the one specified by the specified value. It accepts the following values: ‘none’ Always apply transposition. (default) ‘portrait’ Preserve portrait geometry (when height >= width). ‘landscape’ Preserve landscape geometry (when width >= height).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#transpose_005fnpp

        """
        filter_node = FilterNode(
            name="transpose_npp",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dir": dir,
                "passthrough": passthrough,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def transpose_vt(
        self,
        *,
        dir: int | DefaultStr = DefaultStr("TRANSPOSE_CCLOCK_FLIP"),
        passthrough: int | Literal["none", "portrait", "landscape"] | DefaultStr = DefaultStr("none"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        14.12 transpose_vt
        Transpose rows with columns in the input video and optionally flip it.
        For more in depth examples see the transpose video filter, which shares mostly the same options.

        It accepts the following parameters:

        Parameters:
        ----------

        :param int dir: Specify the transposition direction. Can assume the following values: ‘cclock_flip’ Rotate by 90 degrees counterclockwise and vertically flip. (default) ‘clock’ Rotate by 90 degrees clockwise. ‘cclock’ Rotate by 90 degrees counterclockwise. ‘clock_flip’ Rotate by 90 degrees clockwise and vertically flip. ‘hflip’ Flip the input video horizontally. ‘vflip’ Flip the input video vertically.
        :param int passthrough: Do not apply the transposition if the input geometry matches the one specified by the specified value. It accepts the following values: ‘none’ Always apply transposition. (default) ‘portrait’ Preserve portrait geometry (when height >= width). ‘landscape’ Preserve landscape geometry (when width >= height).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#transpose_005fvt

        """
        filter_node = FilterNode(
            name="transpose_vt",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dir": dir,
                "passthrough": passthrough,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def transpose_vulkan(
        self,
        *,
        dir: int | DefaultStr = DefaultStr("TRANSPOSE_CCLOCK_FLIP"),
        passthrough: int | Literal["none", "portrait", "landscape"] | DefaultStr = DefaultStr("none"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        14.13 transpose_vulkan
        Transpose rows with columns in the input video and optionally flip it.
        For more in depth examples see the transpose video filter, which shares mostly the same options.

        It accepts the following parameters:

        Parameters:
        ----------

        :param int dir: Specify the transposition direction. Can assume the following values: ‘cclock_flip’ Rotate by 90 degrees counterclockwise and vertically flip. (default) ‘clock’ Rotate by 90 degrees clockwise. ‘cclock’ Rotate by 90 degrees counterclockwise. ‘clock_flip’ Rotate by 90 degrees clockwise and vertically flip.
        :param int passthrough: Do not apply the transposition if the input geometry matches the one specified by the specified value. It accepts the following values: ‘none’ Always apply transposition. (default) ‘portrait’ Preserve portrait geometry (when height >= width). ‘landscape’ Preserve landscape geometry (when width >= height).

        Ref: https://ffmpeg.org/ffmpeg-filters.html#transpose_005fvulkan

        """
        filter_node = FilterNode(
            name="transpose_vulkan",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "dir": dir,
                "passthrough": passthrough,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def trim(
        self,
        *,
        start: int | DefaultStr = DefaultStr("9223372036854775807LL"),
        end: int | DefaultStr = DefaultStr("9223372036854775807LL"),
        start_pts: int | DefaultStr = DefaultStr("((int64_t)(0x8000000000000000ULL))"),
        end_pts: int | DefaultStr = DefaultStr("((int64_t)(0x8000000000000000ULL))"),
        duration: int | DefaultInt = DefaultInt(0),
        start_frame: int | DefaultInt = DefaultInt(-1),
        end_frame: int | DefaultStr = DefaultStr("9223372036854775807LL"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.265 trim
        Trim the input so that the output contains one continuous subpart of the input.

        It accepts the following parameters:

        start, end, and duration are expressed as time
        duration specifications; see
        (ffmpeg-utils)the Time duration section in the ffmpeg-utils(1) manual
        for the accepted syntax.

        Note that the first two sets of the start/end options and the duration
        option look at the frame timestamp, while the _frame variants simply count the
        frames that pass through the filter. Also note that this filter does not modify
        the timestamps. If you wish for the output timestamps to start at zero, insert a
        setpts filter after the trim filter.

        If multiple start or end options are set, this filter tries to be greedy and
        keep all the frames that match at least one of the specified constraints. To keep
        only the part that matches all the constraints at once, chain multiple trim
        filters.

        The defaults are such that all the input is kept. So it is possible to set e.g.
        just the end values to keep everything before the specified time.

        Examples:

         Drop everything except the second minute of input:

        ffmpeg -i INPUT -vf trim=60:120

         Keep only the first second:

        ffmpeg -i INPUT -vf trim=duration=1

        Parameters:
        ----------

        :param int start: None
        :param int end: None
        :param int start_pts: None
        :param int end_pts: None
        :param int duration: None
        :param int start_frame: None
        :param int end_frame: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#trim

        """
        filter_node = FilterNode(
            name="trim",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "start": start,
                "end": end,
                "start_pts": start_pts,
                "end_pts": end_pts,
                "duration": duration,
                "start_frame": start_frame,
                "end_frame": end_frame,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def unsharp(
        self,
        *,
        luma_msize_x: int | DefaultInt = DefaultInt(5),
        luma_msize_y: int | DefaultInt = DefaultInt(5),
        luma_amount: float | DefaultFloat = DefaultFloat(1.0),
        chroma_msize_x: int | DefaultInt = DefaultInt(5),
        chroma_msize_y: int | DefaultInt = DefaultInt(5),
        chroma_amount: float | DefaultFloat = DefaultFloat(0.0),
        alpha_msize_x: int | DefaultInt = DefaultInt(5),
        alpha_msize_y: int | DefaultInt = DefaultInt(5),
        alpha_amount: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.267 unsharp
        Sharpen or blur the input video.

        It accepts the following parameters:


        All parameters are optional and default to the equivalent of the
        string ’5:5:1.0:5:5:0.0’.

        Parameters:
        ----------

        :param int luma_msize_x: Set the luma matrix horizontal size. It must be an odd integer between 3 and 23. The default value is 5.
        :param int luma_msize_y: Set the luma matrix vertical size. It must be an odd integer between 3 and 23. The default value is 5.
        :param float luma_amount: Set the luma effect strength. It must be a floating point number, reasonable values lay between -1.5 and 1.5. Negative values will blur the input video, while positive values will sharpen it, a value of zero will disable the effect. Default value is 1.0.
        :param int chroma_msize_x: Set the chroma matrix horizontal size. It must be an odd integer between 3 and 23. The default value is 5.
        :param int chroma_msize_y: Set the chroma matrix vertical size. It must be an odd integer between 3 and 23. The default value is 5.
        :param float chroma_amount: Set the chroma effect strength. It must be a floating point number, reasonable values lay between -1.5 and 1.5. Negative values will blur the input video, while positive values will sharpen it, a value of zero will disable the effect. Default value is 0.0.
        :param int alpha_msize_x: Set the alpha matrix horizontal size. It must be an odd integer between 3 and 23. The default value is 5.
        :param int alpha_msize_y: Set the alpha matrix vertical size. It must be an odd integer between 3 and 23. The default value is 5.
        :param float alpha_amount: Set the alpha effect strength. It must be a floating point number, reasonable values lay between -1.5 and 1.5. Negative values will blur the input video, while positive values will sharpen it, a value of zero will disable the effect. Default value is 0.0.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#unsharp

        """
        filter_node = FilterNode(
            name="unsharp",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "luma_msize_x": luma_msize_x,
                "luma_msize_y": luma_msize_y,
                "luma_amount": luma_amount,
                "chroma_msize_x": chroma_msize_x,
                "chroma_msize_y": chroma_msize_y,
                "chroma_amount": chroma_amount,
                "alpha_msize_x": alpha_msize_x,
                "alpha_msize_y": alpha_msize_y,
                "alpha_amount": alpha_amount,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def unsharp_opencl(
        self,
        *,
        luma_msize_x: float | DefaultFloat = DefaultFloat(5.0),
        luma_msize_y: float | DefaultFloat = DefaultFloat(5.0),
        luma_amount: float | DefaultFloat = DefaultFloat(1.0),
        chroma_msize_x: float | DefaultFloat = DefaultFloat(5.0),
        chroma_msize_y: float | DefaultFloat = DefaultFloat(5.0),
        chroma_amount: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.17 unsharp_opencl
        Sharpen or blur the input video.

        It accepts the following parameters:


        All parameters are optional and default to the equivalent of the
        string ’5:5:1.0:5:5:0.0’.

        Parameters:
        ----------

        :param float luma_msize_x: Set the luma matrix horizontal size. Range is [1, 23] and default value is 5.
        :param float luma_msize_y: Set the luma matrix vertical size. Range is [1, 23] and default value is 5.
        :param float luma_amount: Set the luma effect strength. Range is [-10, 10] and default value is 1.0. Negative values will blur the input video, while positive values will sharpen it, a value of zero will disable the effect.
        :param float chroma_msize_x: Set the chroma matrix horizontal size. Range is [1, 23] and default value is 5.
        :param float chroma_msize_y: Set the chroma matrix vertical size. Range is [1, 23] and default value is 5.
        :param float chroma_amount: Set the chroma effect strength. Range is [-10, 10] and default value is 0.0. Negative values will blur the input video, while positive values will sharpen it, a value of zero will disable the effect.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#unsharp_005fopencl

        """
        filter_node = FilterNode(
            name="unsharp_opencl",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "luma_msize_x": luma_msize_x,
                "luma_msize_y": luma_msize_y,
                "luma_amount": luma_amount,
                "chroma_msize_x": chroma_msize_x,
                "chroma_msize_y": chroma_msize_y,
                "chroma_amount": chroma_amount,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def untile(self, *, layout: str | DefaultStr = DefaultStr("6x5"), **kwargs: Any) -> "VideoStream":
        """

        11.268 untile
        Decompose a video made of tiled images into the individual images.

        The frame rate of the output video is the frame rate of the input video
        multiplied by the number of tiles.

        This filter does the reverse of tile.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str layout: Set the grid size (i.e. the number of lines and columns). For the syntax of this option, check the (ffmpeg-utils)"Video size" section in the ffmpeg-utils manual.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#untile

        """
        filter_node = FilterNode(
            name="untile",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "layout": layout,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def uspp(
        self,
        *,
        quality: int | DefaultInt = DefaultInt(3),
        qp: int | DefaultInt = DefaultInt(0),
        use_bframe_qp: bool | DefaultInt = DefaultInt(0),
        codec: str | DefaultStr = DefaultStr("snow"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.269 uspp
        Apply ultra slow/simple postprocessing filter that compresses and decompresses
        the image at several (or - in the case of quality level 8 - all)
        shifts and average the results.

        The way this differs from the behavior of spp is that uspp actually encodes &
        decodes each case with libavcodec Snow, whereas spp uses a simplified intra only 8x8
        DCT similar to MJPEG.

        This filter is only available in ffmpeg version 4.4 or earlier.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int quality: Set quality. This option defines the number of levels for averaging. It accepts an integer in the range 0-8. If set to 0, the filter will have no effect. A value of 8 means the higher quality. For each increment of that value the speed drops by a factor of approximately 2. Default value is 3.
        :param int qp: Force a constant quantization parameter. If not set, the filter will use the QP from the video stream (if available).
        :param bool use_bframe_qp: None
        :param str codec: Use specified codec instead of snow.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#uspp

        """
        filter_node = FilterNode(
            name="uspp",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "quality": quality,
                "qp": qp,
                "use_bframe_qp": use_bframe_qp,
                "codec": codec,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def v360(
        self,
        *,
        input: int
        | Literal[
            "e",
            "equirect",
            "c3x2",
            "c6x1",
            "eac",
            "dfisheye",
            "flat",
            "rectilinear",
            "gnomonic",
            "barrel",
            "fb",
            "c1x6",
            "sg",
            "mercator",
            "ball",
            "hammer",
            "sinusoidal",
            "fisheye",
            "pannini",
            "cylindrical",
            "tetrahedron",
            "barrelsplit",
            "tsp",
            "hequirect",
            "he",
            "equisolid",
            "og",
            "octahedron",
            "cylindricalea",
        ]
        | DefaultStr = DefaultStr("e"),
        output: int
        | Literal[
            "e",
            "equirect",
            "c3x2",
            "c6x1",
            "eac",
            "dfisheye",
            "flat",
            "rectilinear",
            "gnomonic",
            "barrel",
            "fb",
            "c1x6",
            "sg",
            "mercator",
            "ball",
            "hammer",
            "sinusoidal",
            "fisheye",
            "pannini",
            "cylindrical",
            "perspective",
            "tetrahedron",
            "barrelsplit",
            "tsp",
            "hequirect",
            "he",
            "equisolid",
            "og",
            "octahedron",
            "cylindricalea",
        ]
        | DefaultStr = DefaultStr("c3x2"),
        interp: int
        | Literal[
            "near",
            "nearest",
            "line",
            "linear",
            "lagrange9",
            "cube",
            "cubic",
            "lanc",
            "lanczos",
            "sp16",
            "spline16",
            "gauss",
            "gaussian",
            "mitchell",
        ]
        | DefaultStr = DefaultStr("line"),
        w: int | DefaultInt = DefaultInt(0),
        h: int | DefaultInt = DefaultInt(0),
        in_stereo: int | Literal["2d", "sbs", "tb"] | DefaultStr = DefaultStr("2d"),
        out_stereo: int | Literal["2d", "sbs", "tb"] | DefaultStr = DefaultStr("2d"),
        in_forder: str | DefaultStr = DefaultStr("rludfb"),
        out_forder: str | DefaultStr = DefaultStr("rludfb"),
        in_frot: str | DefaultStr = DefaultStr("000000"),
        out_frot: str | DefaultStr = DefaultStr("000000"),
        in_pad: float | DefaultStr = DefaultStr("0.f"),
        out_pad: float | DefaultStr = DefaultStr("0.f"),
        fin_pad: int | DefaultInt = DefaultInt(0),
        fout_pad: int | DefaultInt = DefaultInt(0),
        yaw: float | DefaultStr = DefaultStr("0.f"),
        pitch: float | DefaultStr = DefaultStr("0.f"),
        roll: float | DefaultStr = DefaultStr("0.f"),
        rorder: str | DefaultStr = DefaultStr("ypr"),
        h_fov: float | DefaultStr = DefaultStr("0.f"),
        v_fov: float | DefaultStr = DefaultStr("0.f"),
        d_fov: float | DefaultStr = DefaultStr("0.f"),
        h_flip: bool | DefaultInt = DefaultInt(0),
        v_flip: bool | DefaultInt = DefaultInt(0),
        d_flip: bool | DefaultInt = DefaultInt(0),
        ih_flip: bool | DefaultInt = DefaultInt(0),
        iv_flip: bool | DefaultInt = DefaultInt(0),
        in_trans: bool | DefaultInt = DefaultInt(0),
        out_trans: bool | DefaultInt = DefaultInt(0),
        ih_fov: float | DefaultStr = DefaultStr("0.f"),
        iv_fov: float | DefaultStr = DefaultStr("0.f"),
        id_fov: float | DefaultStr = DefaultStr("0.f"),
        h_offset: float | DefaultStr = DefaultStr("0.f"),
        v_offset: float | DefaultStr = DefaultStr("0.f"),
        alpha_mask: bool | DefaultInt = DefaultInt(0),
        reset_rot: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.270 v360
        Convert 360 videos between various formats.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int input: Set format of the input/output video. Available formats: ‘e’ ‘equirect’ Equirectangular projection. ‘c3x2’ ‘c6x1’ ‘c1x6’ Cubemap with 3x2/6x1/1x6 layout. Format specific options: in_pad out_pad Set padding proportion for the input/output cubemap. Values in decimals. Example values: ‘0’ No padding. ‘0.01’ 1% of face is padding. For example, with 1920x1280 resolution face size would be 640x640 and padding would be 3 pixels from each side. (640 * 0.01 = 6 pixels) Default value is ‘0’. Maximum value is ‘0.1’. fin_pad fout_pad Set fixed padding for the input/output cubemap. Values in pixels. Default value is ‘0’. If greater than zero it overrides other padding options. in_forder out_forder Set order of faces for the input/output cubemap. Choose one direction for each position. Designation of directions: ‘r’ right ‘l’ left ‘u’ up ‘d’ down ‘f’ forward ‘b’ back Default value is ‘rludfb’. in_frot out_frot Set rotation of faces for the input/output cubemap. Choose one angle for each position. Designation of angles: ‘0’ 0 degrees clockwise ‘1’ 90 degrees clockwise ‘2’ 180 degrees clockwise ‘3’ 270 degrees clockwise Default value is ‘000000’. ‘eac’ Equi-Angular Cubemap. ‘flat’ ‘gnomonic’ ‘rectilinear’ Regular video. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘dfisheye’ Dual fisheye. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘barrel’ ‘fb’ ‘barrelsplit’ Facebook’s 360 formats. ‘sg’ Stereographic format. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘mercator’ Mercator format. ‘ball’ Ball format, gives significant distortion toward the back. ‘hammer’ Hammer-Aitoff map projection format. ‘sinusoidal’ Sinusoidal map projection format. ‘fisheye’ Fisheye projection. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘pannini’ Pannini projection. Format specific options: h_fov Set output pannini parameter. ih_fov Set input pannini parameter. ‘cylindrical’ Cylindrical projection. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘perspective’ Perspective projection. (output only) Format specific options: v_fov Set perspective parameter. ‘tetrahedron’ Tetrahedron projection. ‘tsp’ Truncated square pyramid projection. ‘he’ ‘hequirect’ Half equirectangular projection. ‘equisolid’ Equisolid format. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘og’ Orthographic format. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘octahedron’ Octahedron projection. ‘cylindricalea’ Cylindrical Equal Area projection.
        :param int output: Set format of the input/output video. Available formats: ‘e’ ‘equirect’ Equirectangular projection. ‘c3x2’ ‘c6x1’ ‘c1x6’ Cubemap with 3x2/6x1/1x6 layout. Format specific options: in_pad out_pad Set padding proportion for the input/output cubemap. Values in decimals. Example values: ‘0’ No padding. ‘0.01’ 1% of face is padding. For example, with 1920x1280 resolution face size would be 640x640 and padding would be 3 pixels from each side. (640 * 0.01 = 6 pixels) Default value is ‘0’. Maximum value is ‘0.1’. fin_pad fout_pad Set fixed padding for the input/output cubemap. Values in pixels. Default value is ‘0’. If greater than zero it overrides other padding options. in_forder out_forder Set order of faces for the input/output cubemap. Choose one direction for each position. Designation of directions: ‘r’ right ‘l’ left ‘u’ up ‘d’ down ‘f’ forward ‘b’ back Default value is ‘rludfb’. in_frot out_frot Set rotation of faces for the input/output cubemap. Choose one angle for each position. Designation of angles: ‘0’ 0 degrees clockwise ‘1’ 90 degrees clockwise ‘2’ 180 degrees clockwise ‘3’ 270 degrees clockwise Default value is ‘000000’. ‘eac’ Equi-Angular Cubemap. ‘flat’ ‘gnomonic’ ‘rectilinear’ Regular video. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘dfisheye’ Dual fisheye. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘barrel’ ‘fb’ ‘barrelsplit’ Facebook’s 360 formats. ‘sg’ Stereographic format. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘mercator’ Mercator format. ‘ball’ Ball format, gives significant distortion toward the back. ‘hammer’ Hammer-Aitoff map projection format. ‘sinusoidal’ Sinusoidal map projection format. ‘fisheye’ Fisheye projection. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘pannini’ Pannini projection. Format specific options: h_fov Set output pannini parameter. ih_fov Set input pannini parameter. ‘cylindrical’ Cylindrical projection. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘perspective’ Perspective projection. (output only) Format specific options: v_fov Set perspective parameter. ‘tetrahedron’ Tetrahedron projection. ‘tsp’ Truncated square pyramid projection. ‘he’ ‘hequirect’ Half equirectangular projection. ‘equisolid’ Equisolid format. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘og’ Orthographic format. Format specific options: h_fov v_fov d_fov Set output horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ih_fov iv_fov id_fov Set input horizontal/vertical/diagonal field of view. Values in degrees. If diagonal field of view is set it overrides horizontal and vertical field of view. ‘octahedron’ Octahedron projection. ‘cylindricalea’ Cylindrical Equal Area projection.
        :param int interp: Set interpolation method. Note: more complex interpolation methods require much more memory to run. Available methods: ‘near’ ‘nearest’ Nearest neighbour. ‘line’ ‘linear’ Bilinear interpolation. ‘lagrange9’ Lagrange9 interpolation. ‘cube’ ‘cubic’ Bicubic interpolation. ‘lanc’ ‘lanczos’ Lanczos interpolation. ‘sp16’ ‘spline16’ Spline16 interpolation. ‘gauss’ ‘gaussian’ Gaussian interpolation. ‘mitchell’ Mitchell interpolation. Default value is ‘line’.
        :param int w: Set the output video resolution. Default resolution depends on formats.
        :param int h: Set the output video resolution. Default resolution depends on formats.
        :param int in_stereo: Set the input/output stereo format. ‘2d’ 2D mono ‘sbs’ Side by side ‘tb’ Top bottom Default value is ‘2d’ for input and output format.
        :param int out_stereo: Set the input/output stereo format. ‘2d’ 2D mono ‘sbs’ Side by side ‘tb’ Top bottom Default value is ‘2d’ for input and output format.
        :param str in_forder: None
        :param str out_forder: None
        :param str in_frot: None
        :param str out_frot: None
        :param float in_pad: None
        :param float out_pad: None
        :param int fin_pad: None
        :param int fout_pad: None
        :param float yaw: Set rotation for the output video. Values in degrees.
        :param float pitch: Set rotation for the output video. Values in degrees.
        :param float roll: Set rotation for the output video. Values in degrees.
        :param str rorder: Set rotation order for the output video. Choose one item for each position. ‘y, Y’ yaw ‘p, P’ pitch ‘r, R’ roll Default value is ‘ypr’.
        :param float h_fov: None
        :param float v_fov: None
        :param float d_fov: None
        :param bool h_flip: Flip the output video horizontally(swaps left-right)/vertically(swaps up-down)/in-depth(swaps back-forward). Boolean values.
        :param bool v_flip: Flip the output video horizontally(swaps left-right)/vertically(swaps up-down)/in-depth(swaps back-forward). Boolean values.
        :param bool d_flip: Flip the output video horizontally(swaps left-right)/vertically(swaps up-down)/in-depth(swaps back-forward). Boolean values.
        :param bool ih_flip: Set if input video is flipped horizontally/vertically. Boolean values.
        :param bool iv_flip: Set if input video is flipped horizontally/vertically. Boolean values.
        :param bool in_trans: Set if input video is transposed. Boolean value, by default disabled.
        :param bool out_trans: Set if output video needs to be transposed. Boolean value, by default disabled.
        :param float ih_fov: None
        :param float iv_fov: None
        :param float id_fov: None
        :param float h_offset: Set output horizontal/vertical off-axis offset. Default is set to 0. Allowed range is from -1 to 1.
        :param float v_offset: Set output horizontal/vertical off-axis offset. Default is set to 0. Allowed range is from -1 to 1.
        :param bool alpha_mask: Build mask in alpha plane for all unmapped pixels by marking them fully transparent. Boolean value, by default disabled.
        :param bool reset_rot: Reset rotation of output video. Boolean value, by default disabled.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#v360

        """
        filter_node = FilterNode(
            name="v360",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "input": input,
                "output": output,
                "interp": interp,
                "w": w,
                "h": h,
                "in_stereo": in_stereo,
                "out_stereo": out_stereo,
                "in_forder": in_forder,
                "out_forder": out_forder,
                "in_frot": in_frot,
                "out_frot": out_frot,
                "in_pad": in_pad,
                "out_pad": out_pad,
                "fin_pad": fin_pad,
                "fout_pad": fout_pad,
                "yaw": yaw,
                "pitch": pitch,
                "roll": roll,
                "rorder": rorder,
                "h_fov": h_fov,
                "v_fov": v_fov,
                "d_fov": d_fov,
                "h_flip": h_flip,
                "v_flip": v_flip,
                "d_flip": d_flip,
                "ih_flip": ih_flip,
                "iv_flip": iv_flip,
                "in_trans": in_trans,
                "out_trans": out_trans,
                "ih_fov": ih_fov,
                "iv_fov": iv_fov,
                "id_fov": id_fov,
                "h_offset": h_offset,
                "v_offset": v_offset,
                "alpha_mask": alpha_mask,
                "reset_rot": reset_rot,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def vaguedenoiser(
        self,
        *,
        threshold: float | DefaultFloat = DefaultFloat(2.0),
        method: int | Literal["hard", "soft", "garrote"] | DefaultStr = DefaultStr("garrote"),
        nsteps: int | DefaultInt = DefaultInt(6),
        percent: float | DefaultFloat = DefaultFloat(85.0),
        planes: int | DefaultInt = DefaultInt(15),
        type: int | Literal["universal", "bayes"] | DefaultStr = DefaultStr("universal"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.271 vaguedenoiser
        Apply a wavelet based denoiser.

        It transforms each frame from the video input into the wavelet domain,
        using Cohen-Daubechies-Feauveau 9/7. Then it applies some filtering to
        the obtained coefficients. It does an inverse wavelet transform after.
        Due to wavelet properties, it should give a nice smoothed result, and
        reduced noise, without blurring picture features.

        This filter accepts the following options:

        Parameters:
        ----------

        :param float threshold: The filtering strength. The higher, the more filtered the video will be. Hard thresholding can use a higher threshold than soft thresholding before the video looks overfiltered. Default value is 2.
        :param int method: The filtering method the filter will use. It accepts the following values: ‘hard’ All values under the threshold will be zeroed. ‘soft’ All values under the threshold will be zeroed. All values above will be reduced by the threshold. ‘garrote’ Scales or nullifies coefficients - intermediary between (more) soft and (less) hard thresholding. Default is garrote.
        :param int nsteps: Number of times, the wavelet will decompose the picture. Picture can’t be decomposed beyond a particular point (typically, 8 for a 640x480 frame - as 2^9 = 512 > 480). Valid values are integers between 1 and 32. Default value is 6.
        :param float percent: Partial of full denoising (limited coefficients shrinking), from 0 to 100. Default value is 85.
        :param int planes: A list of the planes to process. By default all planes are processed.
        :param int type: The threshold type the filter will use. It accepts the following values: ‘universal’ Threshold used is same for all decompositions. ‘bayes’ Threshold used depends also on each decomposition coefficients. Default is universal.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#vaguedenoiser

        """
        filter_node = FilterNode(
            name="vaguedenoiser",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "threshold": threshold,
                "method": method,
                "nsteps": nsteps,
                "percent": percent,
                "planes": planes,
                "type": type,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def varblur(
        self,
        _radius: "VideoStream",
        *,
        min_r: int | DefaultInt = DefaultInt(0),
        max_r: int | DefaultInt = DefaultInt(8),
        planes: int | DefaultStr = DefaultStr("0xF"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.272 varblur
        Apply variable blur filter by using 2nd video stream to set blur radius.
        The 2nd stream must have the same dimensions.

        This filter accepts the following options:


        The varblur filter also supports the framesync options.

        Parameters:
        ----------

        :param int min_r: Set min allowed radius. Allowed range is from 0 to 254. Default is 0.
        :param int max_r: Set max allowed radius. Allowed range is from 1 to 255. Default is 8.
        :param int planes: Set which planes to process. By default, all are used.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#varblur

        """
        filter_node = FilterNode(
            name="varblur",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _radius,
            ],
            kwargs={
                "min_r": min_r,
                "max_r": max_r,
                "planes": planes,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def vectorscope(
        self,
        *,
        mode: int
        | Literal["gray", "tint", "color", "color2", "color3", "color4", "color5"]
        | DefaultStr = DefaultStr(0),
        x: int | DefaultInt = DefaultInt(1),
        y: int | DefaultInt = DefaultInt(2),
        intensity: float | DefaultFloat = DefaultFloat(0.004),
        envelope: int | Literal["none", "instant", "peak", "peak+instant"] | DefaultStr = DefaultStr("none"),
        graticule: int | Literal["none", "green", "color", "invert"] | DefaultStr = DefaultStr("none"),
        opacity: float | DefaultFloat = DefaultFloat(0.75),
        flags: str | Literal["white", "black", "name"] | DefaultStr = DefaultStr("name"),
        bgopacity: float | DefaultFloat = DefaultFloat(0.3),
        lthreshold: float | DefaultFloat = DefaultFloat(0.0),
        hthreshold: float | DefaultFloat = DefaultFloat(1.0),
        colorspace: int | Literal["auto", "601", "709"] | DefaultStr = DefaultStr("auto"),
        tint0: float | DefaultFloat = DefaultFloat(0.0),
        tint1: float | DefaultFloat = DefaultFloat(0.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.273 vectorscope
        Display 2 color component values in the two dimensional graph (which is called
        a vectorscope).

        This filter accepts the following options:

        Parameters:
        ----------

        :param int mode: Set vectorscope mode. It accepts the following values: ‘gray’ ‘tint’ Gray values are displayed on graph, higher brightness means more pixels have same component color value on location in graph. This is the default mode. ‘color’ Gray values are displayed on graph. Surrounding pixels values which are not present in video frame are drawn in gradient of 2 color components which are set by option x and y. The 3rd color component is static. ‘color2’ Actual color components values present in video frame are displayed on graph. ‘color3’ Similar as color2 but higher frequency of same values x and y on graph increases value of another color component, which is luminance by default values of x and y. ‘color4’ Actual colors present in video frame are displayed on graph. If two different colors map to same position on graph then color with higher value of component not present in graph is picked. ‘color5’ Gray values are displayed on graph. Similar to color but with 3rd color component picked from radial gradient.
        :param int x: Set which color component will be represented on X-axis. Default is 1.
        :param int y: Set which color component will be represented on Y-axis. Default is 2.
        :param float intensity: Set intensity, used by modes: gray, color, color3 and color5 for increasing brightness of color component which represents frequency of (X, Y) location in graph.
        :param int envelope: ‘none’ No envelope, this is default. ‘instant’ Instant envelope, even darkest single pixel will be clearly highlighted. ‘peak’ Hold maximum and minimum values presented in graph over time. This way you can still spot out of range values without constantly looking at vectorscope. ‘peak+instant’ Peak and instant envelope combined together.
        :param int graticule: Set what kind of graticule to draw. ‘none’ ‘green’ ‘color’ ‘invert’
        :param float opacity: Set graticule opacity.
        :param str flags: Set graticule flags. ‘white’ Draw graticule for white point. ‘black’ Draw graticule for black point. ‘name’ Draw color points short names.
        :param float bgopacity: Set background opacity.
        :param float lthreshold: Set low threshold for color component not represented on X or Y axis. Values lower than this value will be ignored. Default is 0. Note this value is multiplied with actual max possible value one pixel component can have. So for 8-bit input and low threshold value of 0.1 actual threshold is 0.1 * 255 = 25.
        :param float hthreshold: Set high threshold for color component not represented on X or Y axis. Values higher than this value will be ignored. Default is 1. Note this value is multiplied with actual max possible value one pixel component can have. So for 8-bit input and high threshold value of 0.9 actual threshold is 0.9 * 255 = 230.
        :param int colorspace: Set what kind of colorspace to use when drawing graticule. ‘auto’ ‘601’ ‘709’ Default is auto.
        :param float tint0: Set color tint for gray/tint vectorscope mode. By default both options are zero. This means no tint, and output will remain gray.
        :param float tint1: Set color tint for gray/tint vectorscope mode. By default both options are zero. This means no tint, and output will remain gray.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#vectorscope

        """
        filter_node = FilterNode(
            name="vectorscope",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "x": x,
                "y": y,
                "intensity": intensity,
                "envelope": envelope,
                "graticule": graticule,
                "opacity": opacity,
                "flags": flags,
                "bgopacity": bgopacity,
                "lthreshold": lthreshold,
                "hthreshold": hthreshold,
                "colorspace": colorspace,
                "tint0": tint0,
                "tint1": tint1,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def vflip(self, **kwargs: Any) -> "VideoStream":
        """

        11.276 vflip
        Flip the input video vertically.

        For example, to vertically flip a video with ffmpeg:

        ffmpeg -i in.avi -vf "vflip" out.avi

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#vflip

        """
        filter_node = FilterNode(
            name="vflip",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def vflip_vulkan(self, **kwargs: Any) -> "VideoStream":
        """

        14.6 vflip_vulkan
        Flips an image vertically.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#vflip_005fvulkan

        """
        filter_node = FilterNode(
            name="vflip_vulkan",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def vfrdet(self, **kwargs: Any) -> "VideoStream":
        """

        11.277 vfrdet
        Detect variable frame rate video.

        This filter tries to detect if the input is variable or constant frame rate.

        At end it will output number of frames detected as having variable delta pts,
        and ones with constant delta pts.
        If there was frames with variable delta, than it will also show min, max and
        average delta encountered.

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#vfrdet

        """
        filter_node = FilterNode(
            name="vfrdet",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def vibrance(
        self,
        *,
        intensity: float | DefaultFloat = DefaultFloat(0.0),
        rbal: float | DefaultFloat = DefaultFloat(1.0),
        gbal: float | DefaultFloat = DefaultFloat(1.0),
        bbal: float | DefaultFloat = DefaultFloat(1.0),
        rlum: float | DefaultFloat = DefaultFloat(0.072186),
        glum: float | DefaultFloat = DefaultFloat(0.715158),
        blum: float | DefaultFloat = DefaultFloat(0.212656),
        alternate: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.278 vibrance
        Boost or alter saturation.

        The filter accepts the following options:

        Parameters:
        ----------

        :param float intensity: Set strength of boost if positive value or strength of alter if negative value. Default is 0. Allowed range is from -2 to 2.
        :param float rbal: Set the red balance. Default is 1. Allowed range is from -10 to 10.
        :param float gbal: Set the green balance. Default is 1. Allowed range is from -10 to 10.
        :param float bbal: Set the blue balance. Default is 1. Allowed range is from -10 to 10.
        :param float rlum: Set the red luma coefficient.
        :param float glum: Set the green luma coefficient.
        :param float blum: Set the blue luma coefficient.
        :param bool alternate: If intensity is negative and this is set to 1, colors will change, otherwise colors will be less saturated, more towards gray.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#vibrance

        """
        filter_node = FilterNode(
            name="vibrance",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "intensity": intensity,
                "rbal": rbal,
                "gbal": gbal,
                "bbal": bbal,
                "rlum": rlum,
                "glum": glum,
                "blum": blum,
                "alternate": alternate,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def vidstabdetect(
        self,
        *,
        result: str | DefaultStr = DefaultStr("transforms.trf"),
        shakiness: int | DefaultInt = DefaultInt(5),
        accuracy: int | DefaultInt = DefaultInt(15),
        stepsize: int | DefaultInt = DefaultInt(6),
        mincontrast: float | DefaultFloat = DefaultFloat(0.25),
        show: int | DefaultInt = DefaultInt(0),
        tripod: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.274 vidstabdetect
        Analyze video stabilization/deshaking. Perform pass 1 of 2, see
        vidstabtransform for pass 2.

        This filter generates a file with relative translation and rotation
        transform information about subsequent frames, which is then used by
        the vidstabtransform filter.

        To enable compilation of this filter you need to configure FFmpeg with
        --enable-libvidstab.

        This filter accepts the following options:

        Parameters:
        ----------

        :param str result: Set the path to the file used to write the transforms information. Default value is transforms.trf.
        :param int shakiness: Set how shaky the video is and how quick the camera is. It accepts an integer in the range 1-10, a value of 1 means little shakiness, a value of 10 means strong shakiness. Default value is 5.
        :param int accuracy: Set the accuracy of the detection process. It must be a value in the range 1-15. A value of 1 means low accuracy, a value of 15 means high accuracy. Default value is 15.
        :param int stepsize: Set stepsize of the search process. The region around minimum is scanned with 1 pixel resolution. Default value is 6.
        :param float mincontrast: Set minimum contrast. Below this value a local measurement field is discarded. Must be a floating point value in the range 0-1. Default value is 0.3.
        :param int show: Show fields and transforms in the resulting frames. It accepts an integer in the range 0-2. Default value is 0, which disables any visualization.
        :param int tripod: Set reference frame number for tripod mode. If enabled, the motion of the frames is compared to a reference frame in the filtered stream, identified by the specified number. The idea is to compensate all movements in a more-or-less static scene and keep the camera view absolutely still. If set to 0, it is disabled. The frames are counted starting from 1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#vidstabdetect

        """
        filter_node = FilterNode(
            name="vidstabdetect",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "result": result,
                "shakiness": shakiness,
                "accuracy": accuracy,
                "stepsize": stepsize,
                "mincontrast": mincontrast,
                "show": show,
                "tripod": tripod,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def vidstabtransform(
        self,
        *,
        input: str | DefaultStr = DefaultStr("transforms.trf"),
        smoothing: int | DefaultInt = DefaultInt(15),
        optalgo: int | Literal["opt", "gauss", "avg"] | DefaultStr = DefaultStr("opt"),
        maxshift: int | DefaultInt = DefaultInt(-1),
        maxangle: float | DefaultFloat = DefaultFloat(-1.0),
        crop: int | Literal["keep", "black"] | DefaultStr = DefaultStr(0),
        invert: int | DefaultInt = DefaultInt(0),
        relative: int | DefaultInt = DefaultInt(1),
        zoom: float | DefaultFloat = DefaultFloat(0.0),
        optzoom: int | DefaultInt = DefaultInt(1),
        zoomspeed: float | DefaultFloat = DefaultFloat(0.25),
        interpol: int | Literal["no", "linear", "bilinear", "bicubic"] | DefaultStr = DefaultStr(2),
        tripod: bool | DefaultInt = DefaultInt(0),
        debug: bool | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.275 vidstabtransform
        Video stabilization/deshaking: pass 2 of 2,
        see vidstabdetect for pass 1.

        Read a file with transform information for each frame and
        apply/compensate them. Together with the vidstabdetect
        filter this can be used to deshake videos. See also
        http://public.hronopik.de/vid.stab. It is important to also use
        the unsharp filter, see below.

        To enable compilation of this filter you need to configure FFmpeg with
        --enable-libvidstab.

        Parameters:
        ----------

        :param str input: None
        :param int smoothing: None
        :param int optalgo: None
        :param int maxshift: None
        :param float maxangle: None
        :param int crop: None
        :param int invert: None
        :param int relative: None
        :param float zoom: None
        :param int optzoom: None
        :param float zoomspeed: None
        :param int interpol: None
        :param bool tripod: None
        :param bool debug: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#vidstabtransform

        """
        filter_node = FilterNode(
            name="vidstabtransform",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "input": input,
                "smoothing": smoothing,
                "optalgo": optalgo,
                "maxshift": maxshift,
                "maxangle": maxangle,
                "crop": crop,
                "invert": invert,
                "relative": relative,
                "zoom": zoom,
                "optzoom": optzoom,
                "zoomspeed": zoomspeed,
                "interpol": interpol,
                "tripod": tripod,
                "debug": debug,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def vif(self, _reference: "VideoStream", **kwargs: Any) -> "VideoStream":
        """

        11.279 vif
        Obtain the average VIF (Visual Information Fidelity) between two input videos.

        This filter takes two input videos.

        Both input videos must have the same resolution and pixel format for
        this filter to work correctly. Also it assumes that both inputs
        have the same number of frames, which are compared one by one.

        The obtained average VIF score is printed through the logging system.

        The filter stores the calculated VIF score of each frame.

        This filter also supports the framesync options.

        In the below example the input file main.mpg being processed is compared
        with the reference file ref.mpg.


        ffmpeg -i main.mpg -i ref.mpg -lavfi vif -f null -

        Parameters:
        ----------


        Ref: https://ffmpeg.org/ffmpeg-filters.html#vif

        """
        filter_node = FilterNode(
            name="vif",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _reference,
            ],
            kwargs={} | kwargs,
        )
        return filter_node.video(0)

    def vignette(
        self,
        *,
        angle: str | DefaultStr = DefaultStr("PI/5"),
        x0: str | DefaultStr = DefaultStr("w/2"),
        y0: str | DefaultStr = DefaultStr("h/2"),
        mode: int | Literal["forward", "backward"] | DefaultStr = DefaultStr("forward"),
        eval: int | DefaultStr = DefaultStr("EVAL_MODE_INIT"),
        dither: bool | DefaultInt = DefaultInt(1),
        aspect: float | DefaultFloat = DefaultFloat(1.0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.280 vignette
        Make or reverse a natural vignetting effect.

        The filter accepts the following options:

        Parameters:
        ----------

        :param str angle: Set lens angle expression as a number of radians. The value is clipped in the [0,PI/2] range. Default value: "PI/5"
        :param str x0: Set center coordinates expressions. Respectively "w/2" and "h/2" by default.
        :param str y0: Set center coordinates expressions. Respectively "w/2" and "h/2" by default.
        :param int mode: Set forward/backward mode. Available modes are: ‘forward’ The larger the distance from the central point, the darker the image becomes. ‘backward’ The larger the distance from the central point, the brighter the image becomes. This can be used to reverse a vignette effect, though there is no automatic detection to extract the lens angle and other settings (yet). It can also be used to create a burning effect. Default value is ‘forward’.
        :param int eval: Set evaluation mode for the expressions (angle, x0, y0). It accepts the following values: ‘init’ Evaluate expressions only once during the filter initialization. ‘frame’ Evaluate expressions for each incoming frame. This is way slower than the ‘init’ mode since it requires all the scalers to be re-computed, but it allows advanced dynamic expressions. Default value is ‘init’.
        :param bool dither: Set dithering to reduce the circular banding effects. Default is 1 (enabled).
        :param float aspect: Set vignette aspect. This setting allows one to adjust the shape of the vignette. Setting this value to the SAR of the input will make a rectangular vignetting following the dimensions of the video. Default is 1/1.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#vignette

        """
        filter_node = FilterNode(
            name="vignette",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "angle": angle,
                "x0": x0,
                "y0": y0,
                "mode": mode,
                "eval": eval,
                "dither": dither,
                "aspect": aspect,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def vmafmotion(self, *, stats_file: str, **kwargs: Any) -> "VideoStream":
        """

        11.281 vmafmotion
        Obtain the average VMAF motion score of a video.
        It is one of the component metrics of VMAF.

        The obtained average motion score is printed through the logging system.

        The filter accepts the following options:


        Example:

        ffmpeg -i ref.mpg -vf vmafmotion -f null -

        Parameters:
        ----------

        :param str stats_file: If specified, the filter will use the named file to save the motion score of each frame with respect to the previous frame. When filename equals "-" the data is sent to standard output.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#vmafmotion

        """
        filter_node = FilterNode(
            name="vmafmotion",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "stats_file": stats_file,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def w3fdif(
        self,
        *,
        filter: int | Literal["simple", "complex"] | DefaultStr = DefaultStr("complex"),
        mode: int | Literal["frame", "field"] | DefaultStr = DefaultStr("field"),
        parity: int | Literal["tff", "bff", "auto"] | DefaultStr = DefaultStr("auto"),
        deint: int | Literal["all", "interlaced"] | DefaultStr = DefaultStr("all"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.283 w3fdif
        Deinterlace the input video ("w3fdif" stands for "Weston 3 Field
        Deinterlacing Filter").

        Based on the process described by Martin Weston for BBC R&D, and
        implemented based on the de-interlace algorithm written by Jim
        Easterbrook for BBC R&D, the Weston 3 field deinterlacing filter
        uses filter coefficients calculated by BBC R&D.

        This filter uses field-dominance information in frame to decide which
        of each pair of fields to place first in the output.
        If it gets it wrong use setfield filter before w3fdif filter.

        There are two sets of filter coefficients, so called "simple"
        and "complex". Which set of filter coefficients is used can
        be set by passing an optional parameter:

        Parameters:
        ----------

        :param int filter: Set the interlacing filter coefficients. Accepts one of the following values: ‘simple’ Simple filter coefficient set. ‘complex’ More-complex filter coefficient set. Default value is ‘complex’.
        :param int mode: The interlacing mode to adopt. It accepts one of the following values: frame Output one frame for each frame. field Output one frame for each field. The default value is field.
        :param int parity: The picture field parity assumed for the input interlaced video. It accepts one of the following values: tff Assume the top field is first. bff Assume the bottom field is first. auto Enable automatic detection of field parity. The default value is auto. If the interlacing is unknown or the decoder does not export this information, top field first will be assumed.
        :param int deint: Specify which frames to deinterlace. Accepts one of the following values: ‘all’ Deinterlace all frames, ‘interlaced’ Only deinterlace frames marked as interlaced. Default value is ‘all’.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#w3fdif

        """
        filter_node = FilterNode(
            name="w3fdif",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "filter": filter,
                "mode": mode,
                "parity": parity,
                "deint": deint,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def waveform(
        self,
        *,
        mode: int | Literal["row", "column"] | DefaultStr = DefaultStr("column"),
        intensity: float | DefaultFloat = DefaultFloat(0.04),
        mirror: bool | DefaultInt = DefaultInt(1),
        display: int | Literal["overlay", "stack", "parade"] | DefaultStr = DefaultStr("stack"),
        components: int | DefaultInt = DefaultInt(1),
        envelope: int | Literal["none", "instant", "peak", "peak+instant"] | DefaultStr = DefaultStr("none"),
        filter: int
        | Literal["lowpass", "flat", "aflat", "chroma", "color", "acolor", "xflat", "yflat"]
        | DefaultStr = DefaultStr(0),
        graticule: int | Literal["none", "green", "orange", "invert"] | DefaultStr = DefaultStr(0),
        opacity: float | DefaultFloat = DefaultFloat(0.75),
        flags: str | Literal["numbers", "dots"] | DefaultStr = DefaultStr("numbers"),
        scale: int | Literal["digital", "millivolts", "ire"] | DefaultStr = DefaultStr(0),
        bgopacity: float | DefaultFloat = DefaultFloat(0.75),
        tint0: float | DefaultFloat = DefaultFloat(0.0),
        tint1: float | DefaultFloat = DefaultFloat(0.0),
        fitmode: int | Literal["none", "size"] | DefaultStr = DefaultStr(0),
        input: int | Literal["all", "first"] | DefaultStr = DefaultStr("first"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.284 waveform
        Video waveform monitor.

        The waveform monitor plots color component intensity. By default luma
        only. Each column of the waveform corresponds to a column of pixels in the
        source video.

        It accepts the following options:

        Parameters:
        ----------

        :param int mode: Can be either row, or column. Default is column. In row mode, the graph on the left side represents color component value 0 and the right side represents value = 255. In column mode, the top side represents color component value = 0 and bottom side represents value = 255.
        :param float intensity: Set intensity. Smaller values are useful to find out how many values of the same luminance are distributed across input rows/columns. Default value is 0.04. Allowed range is [0, 1].
        :param bool mirror: Set mirroring mode. 0 means unmirrored, 1 means mirrored. In mirrored mode, higher values will be represented on the left side for row mode and at the top for column mode. Default is 1 (mirrored).
        :param int display: Set display mode. It accepts the following values: ‘overlay’ Presents information identical to that in the parade, except that the graphs representing color components are superimposed directly over one another. This display mode makes it easier to spot relative differences or similarities in overlapping areas of the color components that are supposed to be identical, such as neutral whites, grays, or blacks. ‘stack’ Display separate graph for the color components side by side in row mode or one below the other in column mode. ‘parade’ Display separate graph for the color components side by side in column mode or one below the other in row mode. Using this display mode makes it easy to spot color casts in the highlights and shadows of an image, by comparing the contours of the top and the bottom graphs of each waveform. Since whites, grays, and blacks are characterized by exactly equal amounts of red, green, and blue, neutral areas of the picture should display three waveforms of roughly equal width/height. If not, the correction is easy to perform by making level adjustments the three waveforms. Default is stack.
        :param int components: Set which color components to display. Default is 1, which means only luma or red color component if input is in RGB colorspace. If is set for example to 7 it will display all 3 (if) available color components.
        :param int envelope: ‘none’ No envelope, this is default. ‘instant’ Instant envelope, minimum and maximum values presented in graph will be easily visible even with small step value. ‘peak’ Hold minimum and maximum values presented in graph across time. This way you can still spot out of range values without constantly looking at waveforms. ‘peak+instant’ Peak and instant envelope combined together.
        :param int filter: ‘lowpass’ No filtering, this is default. ‘flat’ Luma and chroma combined together. ‘aflat’ Similar as above, but shows difference between blue and red chroma. ‘xflat’ Similar as above, but use different colors. ‘yflat’ Similar as above, but again with different colors. ‘chroma’ Displays only chroma. ‘color’ Displays actual color value on waveform. ‘acolor’ Similar as above, but with luma showing frequency of chroma values.
        :param int graticule: Set which graticule to display. ‘none’ Do not display graticule. ‘green’ Display green graticule showing legal broadcast ranges. ‘orange’ Display orange graticule showing legal broadcast ranges. ‘invert’ Display invert graticule showing legal broadcast ranges.
        :param float opacity: Set graticule opacity.
        :param str flags: Set graticule flags. ‘numbers’ Draw numbers above lines. By default enabled. ‘dots’ Draw dots instead of lines.
        :param int scale: Set scale used for displaying graticule. ‘digital’ ‘millivolts’ ‘ire’ Default is digital.
        :param float bgopacity: Set background opacity.
        :param float tint0: Set tint for output. Only used with lowpass filter and when display is not overlay and input pixel formats are not RGB.
        :param float tint1: Set tint for output. Only used with lowpass filter and when display is not overlay and input pixel formats are not RGB.
        :param int fitmode: Set sample aspect ratio of video output frames. Can be used to configure waveform so it is not streched too much in one of directions. ‘none’ Set sample aspect ration to 1/1. ‘size’ Set sample aspect ratio to match input size of video Default is ‘none’.
        :param int input: Set input formats for filter to pick from. Can be ‘all’, for selecting from all available formats, or ‘first’, for selecting first available format. Default is ‘first’.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#waveform

        """
        filter_node = FilterNode(
            name="waveform",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "intensity": intensity,
                "mirror": mirror,
                "display": display,
                "components": components,
                "envelope": envelope,
                "filter": filter,
                "graticule": graticule,
                "opacity": opacity,
                "flags": flags,
                "scale": scale,
                "bgopacity": bgopacity,
                "tint0": tint0,
                "tint1": tint1,
                "fitmode": fitmode,
                "input": input,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def weave(
        self, *, first_field: int | Literal["top", "t", "bottom", "b"] | DefaultStr = DefaultStr("top"), **kwargs: Any
    ) -> "VideoStream":
        """

        11.285 weave, doubleweave
        The weave takes a field-based video input and join
        each two sequential fields into single frame, producing a new double
        height clip with half the frame rate and half the frame count.

        The doubleweave works same as weave but without
        halving frame rate and frame count.

        It accepts the following option:

        Parameters:
        ----------

        :param int first_field: Set first field. Available values are: ‘top, t’ Set the frame as top-field-first. ‘bottom, b’ Set the frame as bottom-field-first.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#weave_002c-doubleweave

        """
        filter_node = FilterNode(
            name="weave",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "first_field": first_field,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def xbr(self, *, n: int | DefaultInt = DefaultInt(3), **kwargs: Any) -> "VideoStream":
        """

        11.286 xbr
        Apply the xBR high-quality magnification filter which is designed for pixel
        art. It follows a set of edge-detection rules, see
        https://forums.libretro.com/t/xbr-algorithm-tutorial/123.

        It accepts the following option:

        Parameters:
        ----------

        :param int n: Set the scaling dimension: 2 for 2xBR, 3 for 3xBR and 4 for 4xBR. Default is 3.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#xbr

        """
        filter_node = FilterNode(
            name="xbr",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "n": n,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def xcorrelate(
        self,
        _secondary: "VideoStream",
        *,
        planes: int | DefaultInt = DefaultInt(7),
        secondary: int | Literal["first", "all"] | DefaultStr = DefaultStr("all"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.287 xcorrelate
        Apply normalized cross-correlation between first and second input video stream.

        Second input video stream dimensions must be lower than first input video stream.

        The filter accepts the following options:


        The xcorrelate filter also supports the framesync options.

        Parameters:
        ----------

        :param int planes: Set which planes to process.
        :param int secondary: Set which secondary video frames will be processed from second input video stream, can be first or all. Default is all.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#xcorrelate

        """
        filter_node = FilterNode(
            name="xcorrelate",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _secondary,
            ],
            kwargs={
                "planes": planes,
                "secondary": secondary,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def xfade(
        self,
        _xfade: "VideoStream",
        *,
        transition: int
        | Literal[
            "custom",
            "fade",
            "wipeleft",
            "wiperight",
            "wipeup",
            "wipedown",
            "slideleft",
            "slideright",
            "slideup",
            "slidedown",
            "circlecrop",
            "rectcrop",
            "distance",
            "fadeblack",
            "fadewhite",
            "radial",
            "smoothleft",
            "smoothright",
            "smoothup",
            "smoothdown",
            "circleopen",
            "circleclose",
            "vertopen",
            "vertclose",
            "horzopen",
            "horzclose",
            "dissolve",
            "pixelize",
            "diagtl",
            "diagtr",
            "diagbl",
            "diagbr",
            "hlslice",
            "hrslice",
            "vuslice",
            "vdslice",
            "hblur",
            "fadegrays",
            "wipetl",
            "wipetr",
            "wipebl",
            "wipebr",
            "squeezeh",
            "squeezev",
            "zoomin",
            "fadefast",
            "fadeslow",
            "hlwind",
            "hrwind",
            "vuwind",
            "vdwind",
            "coverleft",
            "coverright",
            "coverup",
            "coverdown",
            "revealleft",
            "revealright",
            "revealup",
            "revealdown",
        ]
        | DefaultStr = DefaultStr("fade"),
        duration: int | DefaultInt = DefaultInt(1000000),
        offset: int | DefaultInt = DefaultInt(0),
        expr: str,
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.288 xfade
        Apply cross fade from one input video stream to another input video stream.
        The cross fade is applied for specified duration.

        Both inputs must be constant frame-rate and have the same resolution, pixel format,
        frame rate and timebase.

        The filter accepts the following options:

        Parameters:
        ----------

        :param int transition: Set one of available transition effects: ‘custom’ ‘fade’ ‘wipeleft’ ‘wiperight’ ‘wipeup’ ‘wipedown’ ‘slideleft’ ‘slideright’ ‘slideup’ ‘slidedown’ ‘circlecrop’ ‘rectcrop’ ‘distance’ ‘fadeblack’ ‘fadewhite’ ‘radial’ ‘smoothleft’ ‘smoothright’ ‘smoothup’ ‘smoothdown’ ‘circleopen’ ‘circleclose’ ‘vertopen’ ‘vertclose’ ‘horzopen’ ‘horzclose’ ‘dissolve’ ‘pixelize’ ‘diagtl’ ‘diagtr’ ‘diagbl’ ‘diagbr’ ‘hlslice’ ‘hrslice’ ‘vuslice’ ‘vdslice’ ‘hblur’ ‘fadegrays’ ‘wipetl’ ‘wipetr’ ‘wipebl’ ‘wipebr’ ‘squeezeh’ ‘squeezev’ ‘zoomin’ ‘fadefast’ ‘fadeslow’ ‘hlwind’ ‘hrwind’ ‘vuwind’ ‘vdwind’ ‘coverleft’ ‘coverright’ ‘coverup’ ‘coverdown’ ‘revealleft’ ‘revealright’ ‘revealup’ ‘revealdown’ Default transition effect is fade.
        :param int duration: Set cross fade duration in seconds. Range is 0 to 60 seconds. Default duration is 1 second.
        :param int offset: Set cross fade start relative to first input stream in seconds. Default offset is 0.
        :param str expr: Set expression for custom transition effect. The expressions can use the following variables and functions: X Y The coordinates of the current sample. W H The width and height of the image. P Progress of transition effect. PLANE Currently processed plane. A Return value of first input at current location and plane. B Return value of second input at current location and plane. a0(x, y) a1(x, y) a2(x, y) a3(x, y) Return the value of the pixel at location (x,y) of the first/second/third/fourth component of first input. b0(x, y) b1(x, y) b2(x, y) b3(x, y) Return the value of the pixel at location (x,y) of the first/second/third/fourth component of second input.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#xfade

        """
        filter_node = FilterNode(
            name="xfade",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _xfade,
            ],
            kwargs={
                "transition": transition,
                "duration": duration,
                "offset": offset,
                "expr": expr,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def xfade_opencl(
        self,
        _xfade: "VideoStream",
        *,
        transition: int
        | Literal[
            "custom",
            "fade",
            "wipeleft",
            "wiperight",
            "wipeup",
            "wipedown",
            "slideleft",
            "slideright",
            "slideup",
            "slidedown",
        ]
        | DefaultStr = DefaultStr(1),
        source: str,
        kernel: str,
        duration: int | DefaultInt = DefaultInt(1000000),
        offset: int | DefaultInt = DefaultInt(0),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        12.18 xfade_opencl
        Cross fade two videos with custom transition effect by using OpenCL.

        It accepts the following options:


        The program source file must contain a kernel function with the given name,
        which will be run once for each plane of the output.  Each run on a plane
        gets enqueued as a separate 2D global NDRange with one work-item for each
        pixel to be generated.  The global ID offset for each work-item is therefore
        the coordinates of a pixel in the destination image.

        The kernel function needs to take the following arguments:

         Destination image, __write_only image2d_t.

        This image will become the output; the kernel should write all of it.

         First Source image, __read_only image2d_t.
        Second Source image, __read_only image2d_t.

        These are the most recent images on each input.  The kernel may read from
        them to generate the output, but they can’t be written to.

         Transition progress, float. This value is always between 0 and 1 inclusive.

        Example programs:


         Apply dots curtain transition effect:
        __kernel void blend_images(__write_only image2d_t dst,
                                   __read_only  image2d_t src1,
                                   __read_only  image2d_t src2,
                                   float progress)
        {
            const sampler_t sampler = (CLK_NORMALIZED_COORDS_FALSE |
                                       CLK_FILTER_LINEAR);
            int2  p = (int2)(get_global_id(0), get_global_id(1));
            float2 rp = (float2)(get_global_id(0), get_global_id(1));
            float2 dim = (float2)(get_image_dim(src1).x, get_image_dim(src1).y);
            rp = rp / dim;

            float2 dots = (float2)(20.0, 20.0);
            float2 center = (float2)(0,0);
            float2 unused;

            float4 val1 = read_imagef(src1, sampler, p);
            float4 val2 = read_imagef(src2, sampler, p);
            bool next = distance(fract(rp * dots, &unused), (float2)(0.5, 0.5)) < (progress / distance(rp, center));

            write_imagef(dst, p, next ? val1 : val2);
        }

        Parameters:
        ----------

        :param int transition: Set one of possible transition effects. custom Select custom transition effect, the actual transition description will be picked from source and kernel options. fade wipeleft wiperight wipeup wipedown slideleft slideright slideup slidedown Default transition is fade.
        :param str source: OpenCL program source file for custom transition.
        :param str kernel: Set name of kernel to use for custom transition from program source file.
        :param int duration: Set duration of video transition.
        :param int offset: Set time of start of transition relative to first video.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#xfade_005fopencl

        """
        filter_node = FilterNode(
            name="xfade_opencl",
            input_typings=[StreamType.video, StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
                _xfade,
            ],
            kwargs={
                "transition": transition,
                "source": source,
                "kernel": kernel,
                "duration": duration,
                "offset": offset,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def yadif(
        self,
        *,
        mode: int
        | Literal["send_frame", "send_field", "send_frame_nospatial", "send_field_nospatial"]
        | DefaultStr = DefaultStr("send_frame"),
        parity: int | Literal["tff", "bff", "auto"] | DefaultStr = DefaultStr("auto"),
        deint: int | Literal["all", "interlaced"] | DefaultStr = DefaultStr("all"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.291 yadif
        Deinterlace the input video ("yadif" means "yet another deinterlacing
        filter").

        It accepts the following parameters:

        Parameters:
        ----------

        :param int mode: The interlacing mode to adopt. It accepts one of the following values: 0, send_frame Output one frame for each frame. 1, send_field Output one frame for each field. 2, send_frame_nospatial Like send_frame, but it skips the spatial interlacing check. 3, send_field_nospatial Like send_field, but it skips the spatial interlacing check. The default value is send_frame.
        :param int parity: The picture field parity assumed for the input interlaced video. It accepts one of the following values: 0, tff Assume the top field is first. 1, bff Assume the bottom field is first. -1, auto Enable automatic detection of field parity. The default value is auto. If the interlacing is unknown or the decoder does not export this information, top field first will be assumed.
        :param int deint: Specify which frames to deinterlace. Accepts one of the following values: 0, all Deinterlace all frames. 1, interlaced Only deinterlace frames marked as interlaced. The default value is all.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#yadif

        """
        filter_node = FilterNode(
            name="yadif",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "parity": parity,
                "deint": deint,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def yadif_cuda(
        self,
        *,
        mode: int
        | Literal["send_frame", "send_field", "send_frame_nospatial", "send_field_nospatial"]
        | DefaultStr = DefaultStr("send_frame"),
        parity: int | Literal["tff", "bff", "auto"] | DefaultStr = DefaultStr("auto"),
        deint: int | Literal["all", "interlaced"] | DefaultStr = DefaultStr("all"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.292 yadif_cuda
        Deinterlace the input video using the yadif algorithm, but implemented
        in CUDA so that it can work as part of a GPU accelerated pipeline with nvdec
        and/or nvenc.

        It accepts the following parameters:

        Parameters:
        ----------

        :param int mode: The interlacing mode to adopt. It accepts one of the following values: 0, send_frame Output one frame for each frame. 1, send_field Output one frame for each field. 2, send_frame_nospatial Like send_frame, but it skips the spatial interlacing check. 3, send_field_nospatial Like send_field, but it skips the spatial interlacing check. The default value is send_frame.
        :param int parity: The picture field parity assumed for the input interlaced video. It accepts one of the following values: 0, tff Assume the top field is first. 1, bff Assume the bottom field is first. -1, auto Enable automatic detection of field parity. The default value is auto. If the interlacing is unknown or the decoder does not export this information, top field first will be assumed.
        :param int deint: Specify which frames to deinterlace. Accepts one of the following values: 0, all Deinterlace all frames. 1, interlaced Only deinterlace frames marked as interlaced. The default value is all.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#yadif_005fcuda

        """
        filter_node = FilterNode(
            name="yadif_cuda",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "mode": mode,
                "parity": parity,
                "deint": deint,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def yaepblur(
        self,
        *,
        radius: int | DefaultInt = DefaultInt(3),
        planes: int | DefaultInt = DefaultInt(1),
        sigma: int | DefaultInt = DefaultInt(128),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.293 yaepblur
        Apply blur filter while preserving edges ("yaepblur" means "yet another edge preserving blur filter").
        The algorithm is described in
        "J. S. Lee, Digital image enhancement and noise filtering by use of local statistics, IEEE Trans. Pattern Anal. Mach. Intell. PAMI-2, 1980."

        It accepts the following parameters:

        Parameters:
        ----------

        :param int radius: Set the window radius. Default value is 3.
        :param int planes: Set which planes to filter. Default is only the first plane.
        :param int sigma: Set blur strength. Default value is 128.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#yaepblur

        """
        filter_node = FilterNode(
            name="yaepblur",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "radius": radius,
                "planes": planes,
                "sigma": sigma,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def zmq(self, *, bind_address: str | DefaultStr = DefaultStr("tcp://*:5555"), **kwargs: Any) -> "VideoStream":
        """

        18.34 zmq, azmq
        Receive commands sent through a libzmq client, and forward them to
        filters in the filtergraph.

        zmq and azmq work as a pass-through filters. zmq
        must be inserted between two video filters, azmq between two
        audio filters. Both are capable to send messages to any filter type.

        To enable these filters you need to install the libzmq library and
        headers and configure FFmpeg with --enable-libzmq.

        For more information about libzmq see:
        http://www.zeromq.org/

        The zmq and azmq filters work as a libzmq server, which
        receives messages sent through a network interface defined by the
        bind_address (or the abbreviation "b") option.
        Default value of this option is tcp://localhost:5555. You may
        want to alter this value to your needs, but do not forget to escape any
        ’:’ signs (see filtergraph escaping).

        The received message must be in the form:

        TARGET COMMAND [ARG]

        TARGET specifies the target of the command, usually the name of
        the filter class or a specific filter instance name. The default
        filter instance name uses the pattern ‘Parsed_<filter_name>_<index>’,
        but you can override this by using the ‘filter_name@id’ syntax
        (see Filtergraph syntax).

        COMMAND specifies the name of the command for the target filter.

        ARG is optional and specifies the optional argument list for the
        given COMMAND.

        Upon reception, the message is processed and the corresponding command
        is injected into the filtergraph. Depending on the result, the filter
        will send a reply to the client, adopting the format:

        ERROR_CODE ERROR_REASON
        MESSAGE

        MESSAGE is optional.

        Parameters:
        ----------

        :param str bind_address: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#zmq_002c-azmq

        """
        filter_node = FilterNode(
            name="zmq",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "bind_address": bind_address,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def zoompan(
        self,
        *,
        zoom: str | DefaultStr = DefaultStr("1"),
        x: str | DefaultStr = DefaultStr("0"),
        y: str | DefaultStr = DefaultStr("0"),
        d: str | DefaultStr = DefaultStr("90"),
        s: str | DefaultStr = DefaultStr("hd720"),
        fps: str | DefaultStr = DefaultStr("25"),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.294 zoompan
        Apply Zoom & Pan effect.

        This filter accepts the following options:


        Each expression can contain the following constants:

        Parameters:
        ----------

        :param str zoom: Set the zoom expression. Range is 1-10. Default is 1.
        :param str x: Set the x and y expression. Default is 0.
        :param str y: Set the x and y expression. Default is 0.
        :param str d: Set the duration expression in number of frames. This sets for how many number of frames effect will last for single input image. Default is 90.
        :param str s: Set the output image size, default is ’hd720’.
        :param str fps: Set the output frame rate, default is ’25’.

        Ref: https://ffmpeg.org/ffmpeg-filters.html#zoompan

        """
        filter_node = FilterNode(
            name="zoompan",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "zoom": zoom,
                "x": x,
                "y": y,
                "d": d,
                "s": s,
                "fps": fps,
            }
            | kwargs,
        )
        return filter_node.video(0)

    def zscale(
        self,
        *,
        w: str,
        h: str,
        size: str,
        dither: int | Literal["none", "ordered", "random", "error_diffusion"] | DefaultStr = DefaultStr(0),
        filter: int
        | Literal["point", "bilinear", "bicubic", "spline16", "spline36", "lanczos"]
        | DefaultStr = DefaultStr("bilinear"),
        out_range: int | Literal["input", "limited", "full", "unknown", "tv", "pc"] | DefaultStr = DefaultStr("input"),
        primaries: int
        | Literal[
            "input",
            "709",
            "unspecified",
            "170m",
            "240m",
            "2020",
            "unknown",
            "bt709",
            "bt470m",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "film",
            "bt2020",
            "smpte428",
            "smpte431",
            "smpte432",
            "jedec-p22",
            "ebu3213",
        ]
        | DefaultStr = DefaultStr("input"),
        transfer: int
        | Literal[
            "input",
            "709",
            "unspecified",
            "601",
            "linear",
            "2020_10",
            "2020_12",
            "unknown",
            "bt470m",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "bt709",
            "linear",
            "log100",
            "log316",
            "bt2020-10",
            "bt2020-12",
            "smpte2084",
            "iec61966-2-4",
            "iec61966-2-1",
            "arib-std-b67",
        ]
        | DefaultStr = DefaultStr("input"),
        matrix: int
        | Literal[
            "input",
            "709",
            "unspecified",
            "470bg",
            "170m",
            "2020_ncl",
            "2020_cl",
            "unknown",
            "gbr",
            "bt709",
            "fcc",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "ycgco",
            "bt2020nc",
            "bt2020c",
            "chroma-derived-nc",
            "chroma-derived-c",
            "ictcp",
        ]
        | DefaultStr = DefaultStr("input"),
        in_range: int | Literal["input", "limited", "full", "unknown", "tv", "pc"] | DefaultStr = DefaultStr("input"),
        primariesin: int
        | Literal[
            "input",
            "709",
            "unspecified",
            "170m",
            "240m",
            "2020",
            "unknown",
            "bt709",
            "bt470m",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "film",
            "bt2020",
            "smpte428",
            "smpte431",
            "smpte432",
            "jedec-p22",
            "ebu3213",
        ]
        | DefaultStr = DefaultStr("input"),
        transferin: int
        | Literal[
            "input",
            "709",
            "unspecified",
            "601",
            "linear",
            "2020_10",
            "2020_12",
            "unknown",
            "bt470m",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "bt709",
            "linear",
            "log100",
            "log316",
            "bt2020-10",
            "bt2020-12",
            "smpte2084",
            "iec61966-2-4",
            "iec61966-2-1",
            "arib-std-b67",
        ]
        | DefaultStr = DefaultStr("input"),
        matrixin: int
        | Literal[
            "input",
            "709",
            "unspecified",
            "470bg",
            "170m",
            "2020_ncl",
            "2020_cl",
            "unknown",
            "gbr",
            "bt709",
            "fcc",
            "bt470bg",
            "smpte170m",
            "smpte240m",
            "ycgco",
            "bt2020nc",
            "bt2020c",
            "chroma-derived-nc",
            "chroma-derived-c",
            "ictcp",
        ]
        | DefaultStr = DefaultStr("input"),
        chromal: int
        | Literal["input", "left", "center", "topleft", "top", "bottomleft", "bottom"]
        | DefaultStr = DefaultStr("input"),
        chromalin: int
        | Literal["input", "left", "center", "topleft", "top", "bottomleft", "bottom"]
        | DefaultStr = DefaultStr("input"),
        npl: float | DefaultStr = DefaultStr('__builtin_nanf("0x7fc00000")'),
        agamma: bool | DefaultInt = DefaultInt(1),
        param_a: float | DefaultStr = DefaultStr('__builtin_nanf("0x7fc00000")'),
        param_b: float | DefaultStr = DefaultStr('__builtin_nanf("0x7fc00000")'),
        **kwargs: Any,
    ) -> "VideoStream":
        """

        11.295 zscale
        Scale (resize) the input video, using the z.lib library:
        https://github.com/sekrit-twc/zimg. To enable compilation of this
        filter, you need to configure FFmpeg with --enable-libzimg.

        The zscale filter forces the output display aspect ratio to be the same
        as the input, by changing the output sample aspect ratio.

        If the input image format is different from the format requested by
        the next filter, the zscale filter will convert the input to the
        requested format.

        Parameters:
        ----------

        :param str w: None
        :param str h: None
        :param str size: None
        :param int dither: None
        :param int filter: None
        :param int out_range: None
        :param int primaries: None
        :param int transfer: None
        :param int matrix: None
        :param int in_range: None
        :param int primariesin: None
        :param int transferin: None
        :param int matrixin: None
        :param int chromal: None
        :param int chromalin: None
        :param float npl: None
        :param bool agamma: None
        :param float param_a: None
        :param float param_b: None

        Ref: https://ffmpeg.org/ffmpeg-filters.html#zscale

        """
        filter_node = FilterNode(
            name="zscale",
            input_typings=[StreamType.video],
            output_typings=[StreamType.video],
            inputs=[
                self,
            ],
            kwargs={
                "w": w,
                "h": h,
                "size": size,
                "dither": dither,
                "filter": filter,
                "out_range": out_range,
                "primaries": primaries,
                "transfer": transfer,
                "matrix": matrix,
                "in_range": in_range,
                "primariesin": primariesin,
                "transferin": transferin,
                "matrixin": matrixin,
                "chromal": chromal,
                "chromalin": chromalin,
                "npl": npl,
                "agamma": agamma,
                "param_a": param_a,
                "param_b": param_b,
            }
            | kwargs,
        )
        return filter_node.video(0)
