import pytest
from unittest.mock import patch, MagicMock
import sys
from PIL import Image

# rembg が未インストールの環境でもテストできるよう、未ロード時はモックモジュールを登録
if "rembg" not in sys.modules:
    mock_rembg = MagicMock()
    sys.modules["rembg"] = mock_rembg

from main import AvatarEditorApp

@pytest.fixture(scope="module")
def app():
    """テスト用のAvatarEditorAppインスタンスを生成・破棄するフィクスチャ（モジュール単位）"""
    application = AvatarEditorApp()
    application.withdraw()  # ウィンドウを非表示化
    yield application
    try:
        application.destroy()
    except Exception:
        pass


@pytest.fixture(autouse=True)
def reset_app_state(app):
    """各テスト実行前に topmost を False にリセットするフィクスチャ"""
    app.attributes("-topmost", False)
    app.update()
    assert bool(app.attributes("-topmost")) is False


# ------------------------------------------------------------------------------
# 1. open_image_dialog: ファイル選択ダイアログ (L440)
# ------------------------------------------------------------------------------
def test_open_image_dialog_preserves_topmost_state(app):
    """open_image_dialog 呼び出し後に topmost が False のまま維持されることを検証"""
    with patch("tkinter.filedialog.askopenfilename", return_value=""):
        app.open_image_dialog()

    assert bool(app.attributes("-topmost")) is False, (
        "1. open_image_dialog (L440): ダイアログ後に topmost が True に変更されてしまっています"
    )


# ------------------------------------------------------------------------------
# 2. save_image: 「名前を付けて保存」ダイアログ (L453)
# ------------------------------------------------------------------------------
def test_save_image_dialog_preserves_topmost_state(app):
    """save_image のファイル選択ダイアログ呼び出し後に topmost が維持されることを検証"""
    app.image_path = None
    with patch("tkinter.filedialog.asksaveasfilename", return_value=""):
        app.save_image()

    assert bool(app.attributes("-topmost")) is False, (
        "2. save_image (L453): 保存ダイアログ後に topmost が True に変更されてしまっています"
    )


# ------------------------------------------------------------------------------
# 3. save_image: PermissionError エラーダイアログ (L469)
# ------------------------------------------------------------------------------
def test_save_image_permission_error_preserves_topmost_state(app):
    """save_image で PermissionError が発生した際に topmost が維持されることを検証"""
    app.image_path = "dummy_path.png"
    app.current_img = MagicMock()
    app.current_img.save.side_effect = PermissionError("アクセス拒否")

    with patch("tkinter.messagebox.showerror") as mock_error:
        app.save_image()
        assert mock_error.called

    assert bool(app.attributes("-topmost")) is False, (
        "3. save_image (L469): PermissionError ダイアログ後に topmost が True に変更されてしまっています"
    )


# ------------------------------------------------------------------------------
# 4. save_image: 一般例外 Exception エラーダイアログ (L474)
# ------------------------------------------------------------------------------
def test_save_image_general_error_preserves_topmost_state(app):
    """save_image で一般的な例外が発生した際に topmost が維持されることを検証"""
    app.image_path = "dummy_path.png"
    app.current_img = MagicMock()
    app.current_img.save.side_effect = RuntimeError("保存エラー")

    with patch("tkinter.messagebox.showerror") as mock_error:
        app.save_image()
        assert mock_error.called

    assert bool(app.attributes("-topmost")) is False, (
        "4. save_image (L474): Exception ダイアログ後に topmost が True に変更されてしまっています"
    )


# ------------------------------------------------------------------------------
# 5. load_image: 画像読み込みエラーダイアログ (L410)
# ------------------------------------------------------------------------------
def test_load_image_error_preserves_topmost_state(app):
    """load_image で読み込みエラーが発生した際に topmost が維持されることを検証"""
    with patch("tkinter.messagebox.showerror") as mock_error:
        app.load_image("invalid_non_existent_file.png")
        assert mock_error.called

    assert bool(app.attributes("-topmost")) is False, (
        "5. load_image (L410): エラーダイアログ後に topmost が True に変更されてしまっています"
    )


# ------------------------------------------------------------------------------
# 6. apply_rembg: ImportError (ライブラリ不在) エラーダイアログ (L557)
# ------------------------------------------------------------------------------
def test_apply_rembg_import_error_preserves_topmost_state(app):
    """apply_rembg で ImportError が発生した際に topmost が維持されることを検証"""
    app.current_img = Image.new("RGBA", (10, 10), (255, 0, 0, 255))

    # builtins.__import__ をパッチして rembg インポート時に ImportError を発生させる
    original_import = __import__
    def import_mock(name, *args, **kwargs):
        if name == "rembg" or name.startswith("rembg."):
            raise ImportError("rembgが存在しません")
        return original_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=import_mock), \
         patch("tkinter.messagebox.showerror") as mock_error:
        app.apply_rembg()
        assert mock_error.called

    assert bool(app.attributes("-topmost")) is False, (
        "6. apply_rembg (L557): ImportError ダイアログ後に topmost が True に変更されてしまっています"
    )


# ------------------------------------------------------------------------------
# 7. apply_rembg: 一般例外 Exception エラーダイアログ (L562)
# ------------------------------------------------------------------------------
def test_apply_rembg_general_error_preserves_topmost_state(app):
    """apply_rembg で一般的な例外が発生した際に topmost が維持されることを検証"""
    app.current_img = Image.new("RGBA", (10, 10), (255, 0, 0, 255))

    with patch("rembg.remove", side_effect=RuntimeError("AI実行エラー")), \
         patch("tkinter.messagebox.showerror") as mock_error:
        app.apply_rembg()
        assert mock_error.called

    assert bool(app.attributes("-topmost")) is False, (
        "7. apply_rembg (L562): Exception ダイアログ後に topmost が True に変更されてしまっています"
    )


# ------------------------------------------------------------------------------
# 8. 追加検証: 元々 topmost が True だった場合は True に復元されることを検証
# ------------------------------------------------------------------------------
def test_dialog_restores_true_when_initially_topmost(app):
    """元々最前面が有効だった場合、ダイアログ後に最前面有効が正しく復元されることを検証"""
    app.attributes("-topmost", True)
    assert bool(app.attributes("-topmost")) is True

    with patch("tkinter.filedialog.askopenfilename", return_value=""):
        app.open_image_dialog()

    assert bool(app.attributes("-topmost")) is True, (
        "元々 topmost=True だった場合、ダイアログ後も True に復元されるべきです"
    )
