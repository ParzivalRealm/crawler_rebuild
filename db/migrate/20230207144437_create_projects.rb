class CreateProjects < ActiveRecord::Migration[7.0]
  def change
    create_table :projects do |t|
      t.string :name  
      t.string :description
      t.string :status
      t.string :start_date
      t.string :end_date
      t.string :project_manager
      t.string :project_owner
      t.string :project_team
      t.string :project_budget
      t.string :project_risk
      t.string :project_milestones
      t.string :project_dependencies
      t.string :project_issues
      t.string :project_notes
      t.string :project_attachments
      t.string :project_tasks
      t.string :project_comments
      t.string :project_reports
      t.string :project_timesheets
      t.string :project_invoices
      t.string :project_expenses
      t.timestamps
    end
  end
end
