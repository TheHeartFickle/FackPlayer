from typing import Callable, Optional, List, Any, Tuple, TypeVar
import numpy as np


class DependencyNotSetError(Exception):
    """异常类，表示依赖项未设置或未初始化"""

    def __init__(self, dependency_name: str, message: str = None):
        """
        初始化异常

        Args:
            dependency_name: 未设置的依赖项名称
            message: 可选的额外错误信息。如果未提供，将使用默认信息
        """
        self.dependency_name = dependency_name
        if message is None:
            message = f"依赖项 '{dependency_name}' 未设置或未初始化。请在使用前确保它已被正确设置。"
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"{self.__class__.__name__}(dependency_name={self.dependency_name!r}, message={self.message!r})"


def require_dependencies(*dependency_names: str):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            missing = []
            for name in dependency_names:
                dependency = getattr(self, name, None)
                if dependency is None or not callable(dependency):
                    missing.append(name)

            if missing:
                if len(missing) == 1:
                    raise DependencyNotSetError(missing[0])
                else:
                    raise DependencyNotSetError(
                        ", ".join(missing), f"以下依赖项未设置: {', '.join(missing)}"
                    )

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


T = TypeVar("T")
FrameType = np.ndarray
MatchResult = List[Tuple[int, int, int, int]]


class PatternMatcher:
    def __init__(self):
        self._get_frame: Optional[Callable[[], FrameType]] = None
        self._is_present: Optional[Callable[[FrameType], bool]] = None
        self._multi_template_func: Optional[Callable[[FrameType], MatchResult]] = None

    def print_vision_observer_name(self) -> None:
        name = self._get_frame.__name__ if self._get_frame else "未设置"
        print(f"当前观察者依赖：{name}")

    def set_vision_observer(
        self, observer_method: Callable[[], FrameType]
    ) -> "PatternMatcher":
        """
        观察者依赖注入

        要求: 调用 ObserverMethod() 方法能获取cv2图像

        :param ObserverMethod: 观察者依赖
        """
        self._get_frame = observer_method
        return self

    def print_pattern_detector_name(self) -> None:
        name = self._is_present.__name__ if self._is_present else "未设置"
        print(f"当前判定依赖：{name}")

    def set_pattern_detector(
        self, image_match_method: Callable[[FrameType], bool] = lambda img: True
    ) -> "PatternMatcher":
        """
        判定依赖注入

        要求: 依赖入参为cv2图像, 返回值为bool

        调用 VerifyTarget() 方法以调用此依赖,判定依赖的入参为VisionObserver依赖获取的图像

        :param ImageMatchMethod: 判定依赖
        """
        self._is_present = image_match_method
        return self

    @require_dependencies("_is_present", "_get_frame")
    def verify_target(self) -> bool:
        """
        验证目标是否存在
        """
        return self._is_present(self._get_frame())

    def print_multi_pattern_finder_name(self) -> None:
        name = self._multi_template_func.__name__ if self._multi_template_func else "未设置"
        print(f"当前多模板匹配依赖：{name}")

    def set_multi_pattern_finder(
        self, locate_method: Callable[[FrameType], MatchResult]
    ) -> "PatternMatcher":
        """
        多模板匹配依赖注入

        调用FindAll()方法进行多模板匹配, 返回匹配位置列表

        :param func: 多模板匹配依赖
        """
        self._multi_template_func = locate_method
        return self

    @require_dependencies("_multi_template_func", "_get_frame")
    def find_all(self) -> MatchResult:
        return self._multi_template_func(self._get_frame())
