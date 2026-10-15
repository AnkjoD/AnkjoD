# Cài đặt profile AnkjoD

Giao diện đen–tím, điểm hồng nhạt; lấy cảm hứng Madoka Kaname × Homura Akemi qua ngôi sao và mặt đồng hồ. Không dùng ảnh anime tải từ nguồn ngoài. Kỹ năng hiển thị đúng danh sách bạn cung cấp: Java, Python, ReactJS, Node.js và TypeScript. Không thêm tuổi, nghề nghiệp, nơi sống hay trình độ.

## 1. Đưa lên GitHub

1. Đăng nhập tài khoản **AnkjoD**, tạo repository **AnkjoD** và chọn **Public**. Nếu đã có `AnkjoD/AnkjoD`, dùng repository đó và lưu lại README cũ trước khi thay.
2. Giải nén gói. Đưa **nội dung bên trong thư mục `AnkjoD-profile`** vào thư mục gốc repository, không đưa nguyên thư mục bao ngoài.
3. Giữ đúng cấu trúc sau. Thư mục `.github` có dấu chấm đầu tên; đừng bỏ sót.

```text
AnkjoD/
├── README.md
├── SETUP.md
├── assets/
│   ├── header.gif
│   ├── header.png
│   ├── skills.svg
│   └── stats.svg
├── scripts/
│   ├── make_header.py
│   └── update_stats.py
└── .github/
    └── workflows/
        └── profile-stats.yml
```

4. Commit các file vào nhánh mặc định. Mở `https://github.com/AnkjoD` để xem profile.

Có thể dùng **Add file → Upload files** cho README, SETUP, assets và scripts. Nếu trình duyệt bỏ qua `.github`, dùng **Add file → Create new file**, đặt tên `.github/workflows/profile-stats.yml`, rồi dán nguyên nội dung file workflow trong gói. Không cần GitHub Pages.

Điều kiện README profile theo [tài liệu GitHub](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme): repository công khai trùng tên tài khoản, có `README.md` không rỗng ở thư mục gốc.

## 2. Bật thống kê tự cập nhật

1. Mở repository → **Actions**. Cho phép workflow chạy nếu GitHub yêu cầu.
2. Chọn **Update profile stats → Run workflow** trên nhánh mặc định.
3. Khi chạy thành công, bot ghi lại `assets/stats.svg`. Thẻ ban đầu trong gói đã lấy dữ liệu thật từ API GitHub; lần chạy này làm mới dữ liệu sau khi bạn cài đặt.

Workflow đặt lịch mỗi ngày lúc **07:23 giờ Việt Nam/Thái Lan (UTC+7)**. Lịch GitHub có thể chạy trễ; repository công khai không có hoạt động lâu ngày có thể bị tắt lịch, khi đó mở Actions để bật lại. Số liệu là ảnh chụp tại thời điểm ghi trên thẻ, không phải bộ đếm trực tiếp.

Không cần tự tạo token cá nhân: workflow dùng `GITHUB_TOKEN` sẵn có, quyền `contents: write` để lưu thẻ. Nếu gặp `403` lúc push, kiểm tra **Settings → Actions → General → Workflow permissions** và chính sách repository. Nhánh có quy tắc cấm bot đẩy trực tiếp cần cho phép cập nhật phù hợp với quy tắc của bạn. Nếu chưa bật Actions, hình vẫn hiển thị, chỉ chưa được làm mới.

Thẻ đếm: kho công khai sở hữu (kể cả fork), sao và lượt fork trên các kho sở hữu không phải fork, số người theo dõi. Không đọc kho riêng tư; không suy diễn trình độ từ số liệu. Nếu API lỗi, script dừng và giữ nguyên thẻ cũ. Có thể xem nguồn tại [GitHub REST API](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user) và cách quản lý workflow tại [GitHub Actions](https://docs.github.com/en/actions/tutorials/create-an-example-workflow).

## 3. Chỉnh giao diện và nội dung

| Muốn đổi | Sửa ở đâu |
| --- | --- |
| Dòng chữ dưới banner, liên kết, dự án | `README.md` — có chú thích ẩn cho mục dự án |
| Tên hoặc chữ trên banner | `scripts/make_header.py`, rồi tạo lại ảnh |
| Danh sách kỹ năng | `assets/skills.svg`: sửa tên trong `<text>` và `<title>`; sửa cả `alt` tương ứng trong README |
| Màu thẻ kỹ năng | Các mã màu trong `assets/skills.svg` |
| Màu và nội dung thống kê | `scripts/update_stats.py`, rồi chạy lại workflow |
| Tắt chuyển động | Đổi `assets/header.gif` thành `assets/header.png` trong README |
| Tần suất thống kê | Dòng `cron` trong `.github/workflows/profile-stats.yml` (giờ UTC) |

Bảng màu: nền `#0b0910`, bề mặt `#100d18`, tím `#c3a5ee`, hồng `#eab4c8`, chữ `#eee7f5`. GitHub không cho README đổi nền toàn trang; màu này nằm trong các ảnh và thẻ, vẫn dùng được với theme sáng.

Banner GIF tự lặp, lưu ngay trong repository. Không có máy chủ ảnh động, font từ xa hoặc dịch vụ stats công cộng cần hoạt động mỗi lần mở profile. Các thẻ kỹ năng cũng là SVG cục bộ, không phụ thuộc dịch vụ icon.

### Tạo lại banner trên máy (tùy chọn)

Cần Python 3 và Pillow:

```sh
python -m pip install Pillow
python scripts/make_header.py
```

Script tự tìm font hệ thống phổ biến. Có thể đặt biến môi trường `PROFILE_FONT` và `PROFILE_FONT_BOLD` thành đường dẫn font `.ttf` của bạn. Các font không được đóng gói; ảnh đã xuất sẵn nên không cần cài gì để dùng profile.

Làm mới thống kê trên máy (không cần thư viện thêm):

```sh
python scripts/update_stats.py
```

## 4. Nếu ảnh không hiện

- Kiểm tra đã tải cả thư mục `assets`, tên file đúng chữ hoa/thường và đường dẫn trong README chưa bị đổi.
- Mở ảnh trực tiếp trong repository để xác nhận file tồn tại; commit rồi đợi GitHub cập nhật bộ nhớ đệm.
- Ảnh động không chạy trong một số trình xem Markdown hoặc khi người xem chặn chuyển động. Dùng ảnh PNG nếu muốn.
- Kiểm tra thời điểm trên thẻ stats và lịch sử Actions nếu dữ liệu cũ. Không cần thay số bằng tay.

README, ảnh và mã cập nhật đều nằm trong repository; bạn có thể chỉnh sửa trực tiếp bất cứ lúc nào.

