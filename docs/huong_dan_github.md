# Chuẩn bị đưa lên GitHub

Thư mục này đã gồm README, code, dữ liệu trích, workbook, results, hình và tài liệu. Không có dữ liệu khách hàng, mật khẩu, đường dẫn máy cá nhân trong nội dung project.

## Upload bằng trình duyệt

1. Tạo repository mới tên `life-insurance-pricing-profit-testing`.
2. Upload nội dung **bên trong** thư mục này, giữ nguyên cây thư mục.
3. Kiểm tra README hiển thị hình và liên kết Excel hoạt động.
4. Description gợi ý: “Mô hình định phí tử kỳ và phân tích kịch bản bằng Python/Excel, có đối chiếu kết quả và tài liệu tiếng Việt.”
5. Topics gợi ý: `actuarial`, `life-insurance`, `pricing`, `python`, `excel`, `profit-testing`.

## Dùng Git

Chạy tại thư mục project; thay URL bằng repository thật của bạn:

```bash
git init
git add .
git commit -m "Add term life pricing and profit testing project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/life-insurance-pricing-profit-testing.git
git push -u origin main
```

Project chưa được push hoặc tạo repository online tự động. Các workflow chỉ được chạy trên GitHub sau khi upload.

Không tự chọn giấy phép cho dữ liệu SOA. Nếu muốn cấp phép mã do bạn sở hữu, chọn license cho mã riêng và giữ ghi nhận nguồn bên thứ ba. CONTRIBUTIONS là phần công khai của project.
